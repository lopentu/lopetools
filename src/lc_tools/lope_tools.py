# https://python.langchain.com/en/latest/modules/agents/tools/custom_tools.html#multi-argument-tools
# https://cwngraph.readthedocs.io/en/latest/
import sys

if "../tagger_api" not in sys.path:
    sys.path.append("../tagger_api")
import json
import re

import httpx
from langchain.tools import BaseTool
import opencc
from CwnGraph import CwnImage

from tagger_api.schemas import TagOutput

cwn = CwnImage.latest()
with open("../data/senseid_to_metadata.json", "r") as f:
    asbc_freq = json.load(f)

API_URL = "http://140.112.147.128:8000/api"
t2s = opencc.OpenCC("t2s.json")
s2t = opencc.OpenCC("s2t.json")


class ToolMixin:
    def json_dumps(self, d: dict) -> str:
        return json.dumps(d, default=str, ensure_ascii=False)


class SenseTagTool(BaseTool, ToolMixin):
    name = "SenseTagger"
    description = "輸入文章可以斷詞和標註詞性SenseID和詞義，輸出為JSON格式。"

    def format_text(self, token_dict: dict) -> str | dict:
        token = token_dict["token"]
        tag = token_dict["tag"]
        gloss = token_dict["gloss"]

        gloss = re.sub(r"\(\d\.\d{4}\)", "", gloss)  # remove probability at the end
        m = re.search(r"\[(?P<sense_id>\d{8})\] (?P<gloss>.+。)", gloss)
        if not m:
            sense_id = "NONE"
            gloss = "NONE"
        else:
            sense_id = m.group("sense_id")
            gloss = m.group("gloss")
            # gloss = f"[SenseID] {m.group('sense_id')} || [詞意] {m.group('gloss')}"

        return {
            "詞": token,
            "詞性": tag,
            "SenseID": sense_id,
            "詞意": gloss,
        }
        # return f"([詞] {token} || [詞性] {tag} || {gloss})"

    def _run(self, text: str) -> str:
        with httpx.Client() as client:
            out = []
            response: TagOutput = client.get(
                f"{API_URL}/tag/",
                params={"text": text},
                    timeout=600.0
            ).json()["tagged_text"]
            for sent in response:
                tmp = []
                for tok in sent:
                    tmp.append(
                        # type: ignore
                        self.format_text(tok)
                        # f"([詞] {tok['token']} || [詞性] {tok['tag']} || [詞意] {tok['gloss']})"
                    )
                # out.append("\n".join(tmp))
                out.append(tmp)

            # out = "。".join(out)
            return self.json_dumps(out)

    async def _arun(self, text: str) -> str:
        async with httpx.AsyncClient() as client:
            out = []
            response: TagOutput = (
                await client.get(
                    f"{API_URL}/tag/",
                    params={"text": text},
                    timeout=600.0
                )
            ).json()["tagged_text"]
            for sent in response:
                tmp = []
                for tok in sent:
                    tmp.append(
                        # type: ignore
                        self.format_text(tok)
                        # f"([詞] {tok['token']} || [詞性] {tok['tag']} || [詞意] {tok['gloss']})"
                    )
                out.append("\n".join(tmp))

            # out = "。".join(out)
            return self.json_dumps(out)


class QuerySenseBaseTool(BaseTool, ToolMixin):
    def _base_run(self, text: str, search_method: str) -> str:
        res = {}
        senses = cwn.find_senses(**{search_method: f"^{text}$"})
        for sense in senses:
            res[sense.head_word] = self.expand_sense(sense)

        res = self.json_dumps(res)
        return res

    async def _base_arun(self, text, search_method: str) -> str:
        res = {}
        senses = cwn.find_senses(**{search_method: text})
        for sense in senses:
            res[sense.head_word] = self.expand_sense(sense)

        res = self.json_dumps(res)
        return res

    @staticmethod
    def expand_sense(sense):
        res = {}
        keep = ["definition", "all_examples", "facets", "head_word", "id", "pos"]
        attrs = [
            d
            for d in dir(sense)
            if not d.startswith("__") and not d.startswith("_") and (d in keep)
        ]
        for attr in attrs:
            retrieved = getattr(sense, attr)
            if not retrieved:
                continue
            if callable(retrieved):
                retrieved = retrieved()
            res[attr] = retrieved

        return res


class QuerySenseFromLemmaTool(QuerySenseBaseTool):
    name = "QuerySensesFromLemma"
    description = "搜尋CWN所有詞義，找到lemma符合目標詞的數個詞義，可以使用Regular Expression。輸出為JSON格式。"

    def _run(self, text: str) -> str:
        res = self._base_run(text, "lemma")
        return res

    async def _arun(self, text: str) -> str:
        res = await self._base_arun(text, "lemma")
        return res


class QuerySenseFromDefinitionTool(QuerySenseBaseTool):
    name = "QuerySensesFromDefinition"
    description = "搜尋CWN所有詞義，找到definition有出現目標詞的數個詞義，可以使用Regular Expression。輸出為JSON格式。"

    def _run(self, text: str) -> str:
        res = self._base_run(text, "definition")
        return res

    async def _arun(self, text: str) -> str:
        res = await self._base_arun(text, "definition")
        return res


class QuerySenseFromExamplesTool(QuerySenseBaseTool):
    name = "QuerySensesFromExample"
    description = "搜尋CWN所有詞義，找到例句有出現目標詞的數個詞義，可以使用Regular Expression。輸出為JSON格式。"

    def _run(self, text: str) -> str:
        res = json.loads(self._base_run(text, "examples"))
        for k, v in res.items():
            all_examples = v["all_examples"]
            # 原本一個sense的all_examples(list of strings)改成只收錄符合的例句們
            new_examples = []
            for example in all_examples:
                if re.search(text, example):
                    new_examples.append(example)
            v["all_examples"] = new_examples
            res[k] = v

        return self.json_dumps(res)

    async def _arun(self, text: str) -> str:
        res = json.loads(await self._base_arun(text, "examples"))
        for k, v in res.items():
            all_examples = v["all_examples"]
            # 原本一個sense的all_examples(list of strings)改成只收錄符合的例句們
            new_examples = []
            for example in all_examples:
                if re.search(text, example):
                    new_examples.append(example)
            v["all_examples"] = new_examples
            res[k] = v

        return self.json_dumps(res)


class QueryRelationsFromSenseIdTool(BaseTool, ToolMixin):
    name = "QueryRelationsFromSenseId"
    description = (
        "輸入目標詞的SenseID（8位數字） ，得到目標詞的relations，取得特定的語意關係（synonym同義詞、antonym反義詞、hypernym上位詞、hyponym下位詞）。如果已經有標記過的文章，則使用文章中目標詞的SenseID，再去獲得該SenseID的relations。輸出為JSON格式。"
    )
    ignore = ["has_facet", "is_synset", "generic", "nearsynonym"]

    def _run(self, sense_id: str) -> str:
        relations = cwn.from_sense_id(sense_id).relations
        relations = [r for r in relations if r[0] not in self.ignore]
        return self.json_dumps(relations)

    async def _arun(self, sense_id: str) -> str:
        relations = cwn.from_sense_id(sense_id).relations
        relations = [r for r in relations if r[0] not in self.ignore]
        return self.json_dumps(relations)


class QueryAsbcSenseFrequencyTool(BaseTool, ToolMixin):
    name = "QueryAsbcSenseFrequency"
    description = "輸入目標詞義的Sense ID（8個數字），得到目標詞義在中研院平衡語料庫（ASBC）的詞義頻率。"

    def _run(self, sense_id: str) -> str:
        if sense_id not in asbc_freq:
            return self.json_dumps({"sense_info": "查無此詞義。"})
        return self.json_dumps({"sense_info": asbc_freq[sense_id]})

    async def _arun(self, sense_id: str) -> str:
        if sense_id not in asbc_freq:
            return self.json_dumps({"sense_info": "查無此詞義。"})
        return self.json_dumps({"sense_info": asbc_freq[sense_id]})
