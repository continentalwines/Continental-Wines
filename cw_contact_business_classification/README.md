# Contact Business Classification

**Version:** 18.0.1.0.0  
**Author:** Goja Solutions  
**License:** LGPL-3  
**Category:** Sales / Contacts

---

## Overview

Extends `res.partner` with two configurable business classification attributes — **Group** and **Channel** — and exposes them as grouping dimensions in the standard Sales reports (Order Line Report and Sales Analysis).

---

## Features

- **Group** and **Channel** fields on contacts (Many2one, configurable lists).
- Child contacts automatically **inherit** Group and Channel from their parent; the fields become read-only when a parent is set.
- Changes to a parent propagate to all children through computed-stored fields.
- Sales Administrators can manage available Groups and Channels from **Sales → Configuration → Business Groups / Business Channels**.
- Both fields appear as optional columns and Group By options in the contacts list and search views.
- **Order Line Report** and **Sales Analysis**: pivot grouping and search Group By by *Custom Group* and *Customer Channel*.

---

## Installation

1. Copy (or symlink) the `cw_contact_business_classification` folder into your Odoo addons path.
2. Update the apps list (**Settings → Apps → Update Apps List**).
3. Search for *Contact Business Classification* and click **Install**.

> The module depends on `contacts`, `sales_team`, and `sale`. Ensure the Sales application is installed before installing this module.

---

## Access Rights

| Role | Business Groups / Channels |
|------|---------------------------|
| Sales Administrator (`group_sale_manager`) | Full CRUD |
| Internal User (`group_user`) | Read-only |

Configuration menus are visible only to Sales Administrators.

---

## Demo Data

When installed with demo data, the following records are created:

**Groups:** On-Trade, Off-Trade, Wholesale  
**Channels:** Restaurant, Hotel, Retail, Online

---

## Module Structure

```
cw_contact_business_classification/
├── __init__.py
├── __manifest__.py
├── demo/
│   └── demo.xml
├── models/
│   ├── __init__.py
│   ├── business_group.py
│   ├── business_channel.py
│   ├── res_partner.py
│   ├── sale_order_line.py
│   └── sale_report.py
├── security/
│   └── ir.model.access.csv
└── views/
    ├── business_group_views.xml
    ├── business_channel_views.xml
    ├── res_partner_views.xml
    ├── sale_order_line_views.xml
    └── sale_report_views.xml
```
