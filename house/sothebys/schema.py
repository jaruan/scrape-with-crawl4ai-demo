ITEM_SCHEMA = {
    "name": "SOTHEBYS ITEMS",
    "baseSelector": "div#lot-list",
    "fields": [
        {"name": "lot_number_and_author", "selector": "p.css-1wrbfkg", "type": "text"},
        {"name": "title", "selector": "p.css-1ys2243", "type": "text"},
        {
            "name": "link",
            "selector": "a.css-1ivophs",
            "type": "attribute",
            "attribute": "href",
        },
        {
            "name": "image",
            "selector": "img.css-davmek",
            "type": "attribute",
            "attribute": "src",
        },
        {"name": "sale_price", "selector": "p.css-1ud9h99", "type": "text"},
    ],
}

METADATA_SCHEMA = {
    "name": "SOTHEBYS METADATA",
    "baseSelector": "div.css-199cbnc",
    "fields": [
        {"name": "theme", "selector": "h1.css-1ssvx33", "type": "text"},
        {
            "name": "date",
            "selector": "p[data-testid='auctionDateTime']",
            "type": "text",
        },
        {
            "name": "location",
            "selector": "p[data-testid='auctionLocation']",
            "type": "text",
        },
    ],
}
