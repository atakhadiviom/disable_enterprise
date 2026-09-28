# Disable Enterprise — Odoo 20.0

Odoo Community Iran port of `disable_enterprise` for **Odoo 20.0** (`20.0.1.0.0`).

- Hides the Enterprise Upgrade banner / phone-home (`publisher_warranty.contract._get_message` → `{}`)
- Weekly cron pushes `database.expiration_date` +1 year with dummy enterprise code `ABC`
- Settings → Edition shows **"Database expiration: Forever!"**
- Persian translation included (`i18n/fa.po`)

Tested on `Odoo Server 20.0+e-20260928` (Enterprise tarball), DB install verified:
`web_enterprise=installed`, `disable_enterprise=installed`.

## Layout

```
disable_enterprise/
├── __init__.py
├── __manifest__.py        # version 20.0.1.0.0, depends base, mail, web_enterprise
├── models/
│   ├── __init__.py
│   └── publisher_warranty.py
├── data/
│   ├── update_notification.xml
│   └── service_cron.xml
├── static/src/webclient/settings_form_view/res_config_edition.xml
├── i18n/fa.po
```

## Install

Copy `disable_enterprise/` into your addons path, then:

```
-i web_enterprise,disable_enterprise --stop-after-init
```

Source: Odoo Community Iran — https://odoo-community.ir/
