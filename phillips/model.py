ITEM_SCHEMA = {
    "name": "PHILLIPS Items",
    "baseSelector": "div.seldon-grid-item",
    "fields": [
        {
            "name": "reserve_flag",
            "selector": "span.seldon-object-tile__badge",
            "type": "text",
        },
        {
            "name": "lot_number",
            "selector": "span.seldon-object-tile__lot-number",
            "type": "text",
        },
        {
            "name": "author",
            "selector": "span.seldon-object-tile__maker",
            "type": "text",
        },
        {
            "name": "title",
            "selector": "span.seldon-object-tile__title",
            "type": "text",
        },
        {
            "name": "link",
            "selector": "a.seldon-object-tile",
            "type": "attribute",
            "attribute": "href",
        },
        {
            "name": "image",
            "selector": "img.seldon-seldon-image-img",
            "type": "attribute",
            "attribute": "src",
        },
        {
            "name": "sale_price",
            "selector": "dt:contains('Estimate') + dd.seldon-detail__value",
            "type": "text",
        },
        {
            "name": "purchased_price",
            "selector": "dt:contains('Sold For') + dd.seldon-detail__value",
            "type": "text",
        },
    ],
}

METADATA_SCHEMA = {
    "name": "PHILLIPS Metadata",
    "baseSelector": "div.seldon-sale-header-banner__stack",
    "fields": [
        {
            "name": "online_or_live",
            "selector": "span.seldon-text--badge",
            "type": "text",
        },
        {
            "name": "theme",
            "selector": "span.seldon-text--title1",
            "type": "text",
        },
        {
            "name": "location",
            "selector": "span.seldon-sale-header-banner__location",
            "type": "text",
        },
        {
            "name": "date",
            "selector": "span.seldon-sale-header-banner__date",
            "type": "text",
        },
    ],
}
