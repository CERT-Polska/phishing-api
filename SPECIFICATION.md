Input/Output specification
==========================

## Definitions

* **CERT.PL Warning List** (,,Lista ostrzeżeń CERT Polska'') - list of alerts regarding internet domains that are used to scam data and funds of internet users;
* **CERT.PL Warning List's Push API** (hereinafter referred to as ,,Push API'') - interface that notifies an external web application about changes made in the CERT.PL Warning List (i.e. adding or deleting a domain alert);
* **data consumer** - a user willing to process the data provided within CERT.PL Warning List (either manually or automatically);
* **external web application** - a HTTP web service operated by the data consumer;

## Disclaimer

This service is provided free of charge. The data provided on the CERT.PL Warning List may be accessed, used and processed without obtaining special permission or license. Although we put all efforts in the maintenance of CERT.PL Warning List, there is **no guarantee** regarding the level of service. The service might periodically come unavailable. Moreover, no guarantees about data quality are provided.

## Overall description

The current contents of CERT.PL Warning List is provided at: http://hole.cert.pl/domains/

Using Push API, the data consumer might request us to make a HTTP request to the external web application, notifying about any change on the CERT.PL Warning List.

## Registration process

In order to use the Push API, data consumer is required to register his external web application using the form available at: https://hole-api.cert.pl/register

1. The abovementioned registration page will generate the necessary configuration parameters. The values of these parameters are presented to the data consumer.
2. The data consumer must then set up his external web application that would conform to the requirements described in the next section.
3. The data consumer must configure the required parameters in his external web application as instructed.
4. The data consumer must ensure that:
  * the time on the external web application's server is synchronized and that the time synchronization service (e.g. `ntpd`) is installed;
  * his external web application is hosted under the domain that could be resolved by public DNS;
  * his external web application's server is accessible over the public Internet
5. The data consumer must paste the appropriate endpoint URL in the registration form;
6. Once the endpoint is properly validated, data consumer must click ,,Activate'' in order to enable the production mode for the integration.

## Expected web application structure

In order to be compatible with the Push API, the external web application must properly respond to the kinds of requests described below. Please note that the path inside the external web application, i.e. `<endpoint-path>` might be arbitrarily chosen by the data consumer. The data consumer will have to provide the full URL to the endpoint during the registration process.

### 1. `GET /`
The ,,main page'' request must return any valid HTTP response (status codes 4xx or 5xx are also allowed). Please note that during this check, the path and the query string part will be removed completely (if present).

### 2. `OPTIONS /<endpoint-path>`
This request must return a valid HTTP response with status code 200 OK. The response must contain `X-PUSHAPI-CERT-PL` and `X-PUSHAPI-CERT-PL-UID` headers. The expected values of these headers are provided in the registration form. Please note that during this check, the query string part will be removed from the URL (if present).

### 3. `POST /<endpoint-path>`
The actual notification request will use `Content-Type: application/x-www-form-urlencoded`. The request body will contain a single form field `jwt`. This field will contain a well formed JSON Web Signature, signed using HMAC-SHA-512. The signing key is provided in the registration form.

The validated JWT will unserialize to a JSON object containing the following fields:

| Field name    | Type                        |  Meaning                        |
| ------------- | --------------------------- | ------------------------------- |
| `id`          | number                      | unique identifier of the entry; positive integer  |
| `domain`      | string                      | FQDN of the domain considered malicious    |
| `status`      | string                      | either `blocked` or `unblocked` |

Depending on the value of `status` field, the consumer's system must treat the domain as malicious (`status` = `blocked`) or neutral (`status` = `unblocked`).

The web application must validate the JWT object provided as a `jwt` form field and return 200 OK if it is properly signed, or 403 Forbidden if the object has malformed signature. During the validation process, we will send improperly signed objects to verify if your application would actually reject them.

## Examples

Example notification consumer implementations are provided in the `example/` directory of [CERT-Polska / phishing-api](https://github.com/CERT-Polska/phishing-api/tree/master/example) GitHub project.

