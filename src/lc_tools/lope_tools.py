# https://python.langchain.com/en/latest/modules/agents/tools/custom_tools.html#multi-argument-tools
# https://cwngraph.readthedocs.io/en/latest/
import sys

if "../tagger_api" not in sys.path:
    sys.path.append("../tagger_api")
import json

import httpx
from langchain.tools import BaseTool
import opencc
from CwnGraph import CwnImage
from CwnGraph.cwn_types import CwnLemma

from tagger_api.schemas import TagOutput

cwn = CwnImage.latest()


API_URL = "http://140.112.147.128:8000/api"
t2s = opencc.OpenCC("t2s.json")
s2t = opencc.OpenCC("s2t.json")


class SenseTagTool(BaseTool):
    # name = "词意标注工具"
    name = "SenseTagger"
    # description = "Get Chinese word senses for a given text"
    description = "輸入文章可以斷詞和標註詞義"

    def _run(self, text: str) -> str:
        # text = s2t.convert(text)
        with httpx.Client() as client:
            out = []
            response: TagOutput = client.get(
                f"{API_URL}/tag/",
                params={"text": text},
            ).json()["tagged_text"]
            for sent in response:
                tmp = []
                for tok in sent:
                    tmp.append(
                        f"([詞] {tok['token']} || [詞性] {tok['tag']} || [詞意] {tok['gloss']})"  # type: ignore
                        # f"([token] {tok['token']} || [gloss] {tok['gloss']})"
                    )
                out.append("\n".join(tmp))

            out = "。".join(out)
            # out = t2s.convert(out)
            return out
            # return t2s.convert(json.dumps(response, ensure_ascii=False))

    async def _arun(self, text: str) -> str:
        raise NotImplementedError


class QuerySenseBaseTool(BaseTool):
    @staticmethod
    def expand_sense(sense):
        res = {}
        ignore = [
            "create",
            "cgu",
            "all_relations",
            "relations",
            "lemmas",
            "data",
            "synset",
        ]
        keep = ["definition", "all_examples", "facets", "head_word"]
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
            # if attr in ["facets", "hypernym", "hyponym", "semantic_relations"]:
            # for r in retrieved:

            #     if isinstance(r, collections.Iterable):
            #     res[attr] = expand_sense(r)
            res[attr] = retrieved

        return res

    def _arun(self):
        raise NotImplementedError

    def json_dumps(self, d: dict) -> str:
        return json.dumps(d, default=str, ensure_ascii=False)


class QuerySenseFromLemmaTool(QuerySenseBaseTool):
    name = "QuerySensesFromLemma"
    description = "搜尋在詞條中出現目標詞的詞義，可以使用Regular Expression。"

    def _run(self, text: str) -> str:
        res = {}
        senses = cwn.find_senses(lemma=text)
        for sense in senses:
            res[sense.head_word] = self.expand_sense(sense)

        res = self.json_dumps(res)
        return res


class QuerySenseFromDefinitionTool(QuerySenseBaseTool):
    name = "QuerySensesFromDefinition"
    description = "搜尋在定義中出現目標詞的詞義，可以使用Regular Expression。"

    def _run(self, text: str) -> str:
        res = {}
        senses = cwn.find_senses(definition=text)
        for sense in senses:
            res[sense.head_word] = self.expand_sense(sense)

        res = self.json_dumps(res)
        return res


class QuerySenseFromExamplesTool(QuerySenseBaseTool):
    name = "QuerySensesFromExample"
    description = "搜尋在例句中出現目標詞的詞義，可以使用Regular Expression。"

    def _run(self, text: str) -> str:
        res = {}
        senses = cwn.find_senses(examples=text)
        for sense in senses:
            res[sense.head_word] = self.expand_sense(sense)

        res = self.json_dumps(res)
        return res
