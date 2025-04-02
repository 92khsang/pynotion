from typing import Optional, TYPE_CHECKING, Union

from pydantic import UUID4

from pynotion.client.sync import NotionSyncClient
from pynotion.core.utils import dump_rx, dump_tx
from pynotion.models.property.rx import RX_PROPERTY_VALUE_CLASS_MAP

if TYPE_CHECKING:
    from pynotion.models import (
        PropertyItemPagination,
        RxPage,
        RxPropertyValue,
        TxPagination,
        TxPage,
        TxPropertyValue,
        ExternalFile,
    )


class PageSyncEndPoint:

    def __init__(self, client: NotionSyncClient):
        self._client = client

    def create_page(self, /, page: "TxPage") -> "RxPage":
        """
        Creates a new page in Notion.

        Args:
            page (TxPage): The page data to be created.

        Returns:
            RxPage: The created page data returned from Notion.
        """
        body = dump_tx(page)
        data = self._client.post("/pages", body=body)
        return dump_rx("RxPage", data)

    def retrieve_page(self, /, page_id: UUID4) -> "RxPage":
        """
        Retrieves a page in Notion.

        Args:
            page_id (UUID4): The page id.

        Returns:
            RxPage: The page data returned from Notion.
        """
        data = self._client.get(f"/pages/{page_id}")
        return dump_rx("RxPage", data)

    def retrieve_page_property_item(
        self,
        /,
        page_id: UUID4,
        property_id: str,
        pagination: Optional["TxPagination"] = None,
    ) -> Union["PropertyItemPagination", "RxPropertyValue"]:
        """
        Retrieves the value of a property item in a page.

        Args:
            page_id (UUID4): The page id.
            property_id (str): The property id.
            pagination (Optional[TxPagination], optional): The pagination. Defaults to None.

        Returns:
            Union[PropertyItemPagination, RxPropertyValue]: The property item pagination or property value.
        """
        __property_item_mapping__ = {
            "property_item": "PropertyItemPagination",
            **RX_PROPERTY_VALUE_CLASS_MAP,
        }

        params = dump_tx(pagination)
        data = self._client.get(
            f"/pages/{page_id}/properties/{property_id}", params=params
        )

        type_value = data.get("type", None)
        if type_value not in __property_item_mapping__:
            raise ValueError(f"Invalid type: {type_value}")

        return dump_rx(
            __property_item_mapping__[type_value], data, discriminator="type"
        )

    def update_page(
        self,
        /,
        page_id: UUID4,
        properties: Optional[dict[str, "TxPropertyValue"]] = None,
        icon: Optional["ExternalFile | NotionEmoji"] = None,
        cover: Optional["ExternalFile"] = None,
    ) -> "RxPage":
        """
        Updates a page.

        Args:
            page_id (UUID4): The page id.
            properties (Optional[dict[str, TxPropertyValue]], optional): The properties. Defaults to None.
            icon (Optional[ExternalFile | NotionEmoji], optional): The icon. Defaults to None.
            cover (Optional[ExternalFile], optional): The cover. Defaults to None.

        Returns:
            RxPage: The updated page.
        """
        body = {}

        if properties:
            body["properties"] = {k: dump_tx(v) for k, v in properties.items()}

        if icon:
            body["icon"] = dump_tx(icon)

        if cover:
            body["cover"] = dump_tx(cover)

        data = self._client.patch(f"/pages/{page_id}", body=body)
        return dump_rx("RxPage", data)

    def delete_page(self, /, page_id: UUID4) -> "RxPage":
        """
        Archives a page in Notion.

        Args:
            page_id (UUID4): The unique identifier of the page to be archived.

        Returns:
            RxPage: The archived page data returned from Notion.
        """
        body = {
            "archived": True,
        }

        data = self._client.patch(f"/pages/{page_id}", body=body)
        return dump_rx("RxPage", data)

    def restore_page(self, /, page_id: UUID4) -> "RxPage":
        """
        Restores an archived page in Notion.

        Args:
            page_id (UUID4): The unique identifier of the page to be restored.

        Returns:
            RxPage: The restored page data returned from Notion.
        """

        body = {
            "archived": False,
        }

        data = self._client.patch(f"/pages/{page_id}", body=body)
        return dump_rx("RxPage", data)
