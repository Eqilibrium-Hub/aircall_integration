# Odoo 15 Aircall integration

⚠️ This is an unofficial aircall integration

## Features

### Log your calls

The system will automatically log your call, 30 seconds after it has ended.
It includes :
- direction of the call
- the agent who made the call
- a recording if present
- metadata such as duration, timestamp ...

![image](https://user-images.githubusercontent.com/79719146/158392125-97e2904a-4f76-4196-85cd-8ddfc8ec5c56.png)

![image](https://user-images.githubusercontent.com/79719146/158392638-36f4d90b-c7b4-4ce7-baad-879f4dab2b75.png)

> 🚧 [TODO] Improve the views

### Insight card support

When an agent operates a call, an insight card will show him information on the client, if the client can be identified by odoo.

![aircall_demo](https://user-images.githubusercontent.com/79719146/158408966-c21ee75d-1829-40c8-af3c-4cd198ae0fe1.gif)

> 🚧 [TODO] Gather more data in the insight card

## Requirements

**Odoo modules** :
- `omar_audio` odoo widget to play a recording (https://apps.odoo.com/apps/modules/15.0/omar_audio/)
- `contacts` you can install it directly in the apps

**Python**:
- `phonenumbers` library, use `pip install phonenumbers` to install

**Aircall** :
- An account and a number, you can get a free trial [here](https://aircall.io/fr/signup/)

**Odoo server** :
- ⚠️ Your odoo server has to be reachable, with at least a public ip adress. If you run a local instance, this will not work
- ⚠️ Your odoo server has to support the HTTPS protocol. This is because aircall webhooks only support HTTPS

**Phone numbers** :
- Phone numbers in the phone field of the contact form in odoo have to be in the INTERNATIONAL format, or else the integration will not work.

## Get started

Install this module as you would do with any module.

The first step is to create an integration in Aircall. 
- Browse the available integrations in the *discover integration section*, and create a *webhook* integration.
- Fill the webhook name with `odoo`, and fill the URL field with 'https://{MyOdooDomain.com}/aircall/webhook'

![image](https://user-images.githubusercontent.com/79719146/158419636-2c2253d0-c90f-4242-9b3b-fc43e49927e6.png)

Check only the following webhooks : 

![image](https://user-images.githubusercontent.com/79719146/160614949-48cf5582-916c-4656-85b5-517ceb7b2402.png)

Next, you will need to configure the odoo module.
- Fill the `API id`, `API token` and `Integration Token` in the **Configuration > Settings** menu 
  - The `Integration Token` is in the webhook integration you've just created
  - You can create an API key (id + token) in **Integrations & API > API keys**

That is all !

## Complementary features

You can set a cron to automatically delete calls older than x hours in **Settings**.

The phone field in the contacts form now only accepts non-ambiguous phone numbers.

You can create a contact marked as a prospect directly from a call log.

## Roadmap

- [ ] Synchronize contacts between odoo and aircall
- [ ] Add a limit to the capacity storage of the logs (recordings can flood the database)
- [ ] Whitelist of users not to log call
- [ ] Make some tests












