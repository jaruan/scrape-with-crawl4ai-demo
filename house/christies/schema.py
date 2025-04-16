ITEM_SCHEMA = {
    "name": "CHRISTIES ITEMS",
    "baseSelector": "li.chr-browse-lot-tile-wrapper",
    "fields": [
        {
            "name": "lot_number",
            "selector": "span.chr-lot-tile__number",
            "type": "text",
        },
        {
            "name": "author",
            "selector": "h2.chr-lot-tile__primary-title",
            "type": "text",
        },
        {
            "name": "title",
            "selector": "p.chr-lot-tile__secondary-title",
            "type": "text",
        },
        {
            "name": "link",
            "selector": "a.chr-lot-tile__link",
            "type": "attribute",
            "attribute": "href",
        },
        {
            "name": "image",
            "selector": "img.chr-img",
            "type": "attribute",
            "attribute": "src",
        },
        {
            "name": "sale_price",
            "selector": "span.chr-lot-tile__price-value",
            "type": "text",
        },
        {
            "name": "purchased_price",
            "selector": "span.chr-lot-tile__secondary-price-value",
            "type": "text",
        },
    ],
}

METADATA_SCHEMA = {
    "name": "CHRISTIES AUCTION METADATA",
    "baseSelector": "div.chr-auction-header-next__main",
    "fields": [
        {
            "name": "online_or_live_and_date",
            "selector": "div.chr-auction-header-next__auction-status",
            "type": "text",
        },
        {
            "name": "theme",
            "selector": "h1.chr-auction-header-next__auction-title",
            "type": "text",
        },
        {
            "name": "location",
            "selector": "div.chr-auction-header-next__viewing-info",
            "type": "text",
        },
    ],
}
