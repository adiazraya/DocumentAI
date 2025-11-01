# Data Cloud Ingestion Feature

## Overview

The Document AI application now automatically ingests extracted data into Salesforce Data Cloud after processing documents. This enables seamless data flow from document extraction to your Data Cloud analytics.

## How It Works

### Automatic Flow

```
1. Document Upload → 2. AI Extraction → 3. Data Cloud Token → 4. Ingestion → 5. Results Display
```

1. **Document Processing**: User uploads document, AI extracts structured data
2. **Token Exchange**: System exchanges Salesforce token for Data Cloud token
3. **Data Transformation**: Adds EventID (UUID) and eventime (current timestamp)
4. **Ingestion**: POSTs data to Data Cloud streaming ingestion API
5. **Response**: Returns both extracted data and ingestion status

### Data Transformation

**Input** (from Document AI):
```json
{
  "Evento": {
    "type": "string",
    "value": "WT 25"
  },
  "LeadsTable": {
    "type": "array",
    "value": [
      {
        "type": "object",
        "value": {
          "Firstname": {"type": "string", "value": "Alberto"},
          "Lastname": {"type": "string", "value": "Diaz"},
          "Email": {"type": "string", "value": "alberto@example.com"},
          "Date": {"type": "string", "value": "20-01-2025"},
          "Company": {"type": "string", "value": "Salesforce"}
        }
      }
    ]
  }
}
```

**Output** (sent to Data Cloud):
```json
{
  "data": [
    {
      "EventID": "550e8400-e29b-41d4-a716-446655440000",
      "eventime": "2025-01-31T10:30:45.000Z",
      "Firstname": "Alberto",
      "Lastname": "Diaz",
      "Email": "alberto@example.com",
      "Date": "20-01-2025",
      "Company": "Salesforce"
    }
  ]
}
```

## Configuration

### 1. Set Up Data Cloud Ingestion Source

In your Salesforce Data Cloud org:
1. Navigate to **Data Cloud** → **Data Streams**
2. Create a new **Ingestion API** source
3. Define your schema matching the OpenAPISpec.yaml
4. Note the **API Name** (e.g., `Lead_Extraction__dll`)

### 2. Configure in Application

1. Go to **⚙️ Configuration** page
2. Scroll to **☁️ Data Cloud Ingestion** section
3. Enter your **Data Cloud Source API Name**
4. Click **💾 Save Configuration**

### Configuration Fields

- **Data Cloud Connector Name**: The connector name in your Data Cloud ingestion path
  - Default: `ContactIngestion`
  - Format: Must match your Data Cloud connector exactly
  - Example: `ContactIngestion`, `LeadIngestion`, `MyConnector`

- **Data Cloud Object Name**: The object name in your Data Cloud ingestion path
  - Default: `LeadRecord`
  - Format: Must match your Data Cloud object exactly
  - Example: `LeadRecord`, `ContactRecord`, `MyObject`

- **Complete Path**: `api/v1/ingest/sources/{connector_name}/{object_name}`

## API Details

### Token Exchange

**Endpoint**: `https://{instance_url}/services/a360/token`

**Method**: POST

**Headers**:
```
Content-Type: application/x-www-form-urlencoded
```

**Body**:
```
grant_type=urn:salesforce:grant-type:external:cdp
subject_token={salesforce_access_token}
subject_token_type=urn:ietf:params:oauth:token-type:access_token
```

**Response**:
```json
{
  "access_token": "eyJraWQi...",
  "instance_url": "grrtsytbg43tmylgg-3w8yzqgh.c360a.salesforce.com",
  "token_type": "Bearer",
  "issued_token_type": "urn:ietf:params:oauth:token-type:jwt",
  "expires_in": 28794
}
```

### Data Ingestion

**Endpoint**: `https://{dc_instance_url}/api/v1/ingest/sources/{connector_name}/{object_name}`

**Method**: POST

**Path Parameters**:
- `connector_name`: Your Data Cloud connector name (e.g., `ContactIngestion`)
- `object_name`: Your Data Cloud object name (e.g., `LeadRecord`)
- **Full path example**: `api/v1/ingest/sources/ContactIngestion/LeadRecord`

**Headers**:
```
Content-Type: application/json
Authorization: Bearer {data_cloud_token}
```

**Body**:
```json
{
  "data": [
    {
      "EventID": "uuid-here",
      "eventime": "2025-01-31T10:30:45.000Z",
      ...other fields
    }
  ]
}
```

## Response Format

The application returns the extracted data with an additional `_ingestion_status` field:

```json
{
  "Evento": {
    "type": "string",
    "value": "WT 25"
  },
  "LeadsTable": {
    "type": "array",
    "value": [...]
  },
  "_ingestion_status": {
    "success": true,
    "records_ingested": 2,
    "response": {}
  }
}
```

### Ingestion Status Fields

- **success** (boolean): Whether ingestion succeeded
- **records_ingested** (number): Count of records sent to Data Cloud
- **response** (object): Response from Data Cloud API
- **error** (string): Error message if ingestion failed
- **status_code** (number): HTTP status code if ingestion failed

## Error Handling

The application uses graceful error handling:

### Ingestion Failure Won't Block Extraction

- If Data Cloud ingestion fails, extraction results are still returned
- Ingestion status indicates the failure
- User can see extracted data even if ingestion fails
- Errors are logged to console and server logs

### Common Issues

#### Token Exchange Fails
```json
{
  "_ingestion_status": null
}
```
**Cause**: Cannot get Data Cloud token
**Solution**: Check Salesforce authentication and permissions

#### Ingestion Fails
```json
{
  "_ingestion_status": {
    "success": false,
    "error": "API error message",
    "status_code": 400
  }
}
```
**Causes**:
- Invalid source API name
- Schema mismatch
- Invalid data format
- Network issues

## Schema Requirements

### OpenAPISpec.yaml

Your Data Cloud source must accept this schema:

```yaml
LeadRedord:
  type: object
  properties:
    EventID:
      type: string
    eventime:
      type: string
      format: date-time
    Firstname:
      type: string
    Lastname:
      type: string
    Email:
      type: string
      format: email
    Date:
      type: string
      format: date
    Company:
      type: string
```

### Required Fields

The application automatically adds:
- **EventID**: Random UUID v4
- **eventime**: Current UTC timestamp in ISO format

### Custom Fields

All other fields from your extraction schema are included as-is.

## Logging

The application logs ingestion activity:

### Success
```
================================================================================
DATA CLOUD TOKEN EXCHANGE REQUEST
================================================================================
Token URL: https://example.salesforce.com/services/a360/token
Headers: { "Content-Type": "application/x-www-form-urlencoded" }
Request Body:
  grant_type: urn:salesforce:grant-type:external:cdp
  subject_token: 00DWV000005ttPB!AQ...
  subject_token_type: urn:ietf:params:oauth:token-type:access_token
================================================================================
DATA CLOUD TOKEN EXCHANGE RESPONSE
================================================================================
Status Code: 200
Response Body:
  access_token: eyJraWQi...
  instance_url: grrtsytbg43tmylgg-3w8yzqgh.c360a.salesforce.com
  token_type: Bearer
  expires_in: 28794 seconds
Successfully obtained Data Cloud token
================================================================================
DATA CLOUD INGESTION REQUEST
================================================================================
Ingestion URL: https://dc-instance.c360a.salesforce.com/api/v1/ingest/sources/ContactIngestion/LeadRecord
Connector Name: ContactIngestion
Object Name: LeadRecord
Records to ingest: 2
Headers:
  Content-Type: application/json
  Authorization: Bearer eyJraWQi...
Payload:
{ "data": [...] }
================================================================================
DATA CLOUD INGESTION RESPONSE
================================================================================
Status Code: 200
Response Body: {...}
================================================================================
✓ Data successfully ingested to Data Cloud
```

### Failure
```
ERROR: Response Body: {"error":"invalid_grant"}
ERROR: Failed to get Data Cloud token: 401
================================================================================
✗ Could not obtain Data Cloud token, skipping ingestion
```

```
ERROR: Response Body: {"error":"Invalid connector or object name"}
✗ Data Cloud ingestion failed: 400
================================================================================
✗ Data Cloud ingestion failed: Invalid connector or object name
```

## Best Practices

### 1. Test Your Source First

Before using the app, test your Data Cloud ingestion endpoint:
```bash
curl --location 'https://{dc_instance}/api/v1/ingest/sources/{connector_name}/{object_name}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {token}' \
--data '{
  "data": [{
    "EventID": "test-123",
    "eventime": "2025-01-31T10:00:00.000Z",
    "Firstname": "Test"
  }]
}'
```

Example:
```bash
curl --location 'https://dc-instance.c360a.salesforce.com/api/v1/ingest/sources/ContactIngestion/LeadRecord' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJraWQi...' \
--data '{
  "data": [{
    "EventID": "550e8400-e29b-41d4-a716-446655440000",
    "eventime": "2025-01-31T10:00:00.000Z",
    "Firstname": "Alberto",
    "Lastname": "Diaz",
    "Email": "alberto@example.com"
  }]
}'
```

### 2. Match Your Schema

Ensure your extraction schema matches your Data Cloud source schema exactly.

### 3. Monitor Logs

Check server logs for ingestion issues:
```bash
tail -f server.log | grep "Data Cloud"
```

### 4. Handle Failures Gracefully

The app will continue working even if ingestion fails. Monitor the `_ingestion_status` field in responses.

## Troubleshooting

### "Could not obtain Data Cloud token"

**Check**:
1. Salesforce authentication is valid
2. User has Data Cloud access
3. Instance URL is correct
4. Network connectivity

### "Data Cloud ingestion failed"

**Check**:
1. Connector name and object name are correct
2. Connector and object exist in Data Cloud
3. Path format is correct: `api/v1/ingest/sources/{connector}/{object}`
4. Schema matches source definition
5. Data Cloud permissions
6. Data Cloud token hasn't expired

### No Ingestion Status in Response

**Possible Causes**:
- Data Cloud feature disabled
- Configuration missing
- Server error during ingestion

**Check**: Server logs for detailed error messages

## Security

### Token Handling

- Salesforce token stays on server
- Data Cloud token obtained on-demand
- Tokens never sent to client
- Token exchange happens per request

### Data Privacy

- Data only sent to configured Data Cloud org
- No third-party data sharing
- All communication over HTTPS
- Tokens short-lived and auto-expiring

## Performance

### Impact

- **Extraction time**: No change
- **Additional time**: ~1-2 seconds for token exchange + ingestion
- **Total overhead**: Minimal (2-3 seconds)
- **Async processing**: Could be added if needed

### Optimization Tips

1. **Token Caching**: Could implement token caching (28+ min lifetime)
2. **Async Ingestion**: Could make ingestion async for faster response
3. **Batch Processing**: Currently processes all records at once

## Future Enhancements

Potential improvements:
- 🔄 Token caching for better performance
- 📊 Ingestion statistics dashboard
- ⚙️ Toggle ingestion on/off in UI
- 📝 Ingestion history tracking
- 🔔 Ingestion failure notifications
- 🔁 Retry logic for failed ingestions
- 📦 Batch size configuration

## Conclusion

The Data Cloud ingestion feature provides seamless integration between document extraction and data analytics, enabling automated data pipelines without manual data entry or export/import steps.

