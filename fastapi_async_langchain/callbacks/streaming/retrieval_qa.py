from typing import Any, Dict

from .base import AsyncLLMChainStreamingCallback

SOURCE_DOCUMENT_TEMPLATE = """
page content: {page_content}
source: {source}
"""


class AsyncRetrievalQAStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for RetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if outputs["source_documents"] is not None:
            await self.send("\n\nSOURCE DOCUMENTS: \n")
            for doc in outputs["source_documents"]:
                await self.send(
                    self.source_document_template.format(
                        page_content=doc.page_content, source=doc.metadata["source"]
                    )
                )