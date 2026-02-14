# Explorium Prospects — Match prospects

Endpoint:
- `POST https://api.explorium.ai/v1/prospects/match`

Headers:
- `Content-Type: application/json`
- `api_key: <api-key>` (required)
- `tenant: <string>` (optional; depends on account)

Body:

```json
{
  "prospects_to_match": [
    {
      "business_id": "<optional>",
      "full_name": "<string|null>",
      "company_name": "<string|null>",
      "email": "<string|null>",
      "phone_number": "<string|null>",
      "linkedin": "<string|null>"
    }
  ],
  "request_context": null
}
```

Constraints:
- `prospects_to_match` length: **1–50**
- If using name+company matching: `full_name` must be accompanied by `company_name` and vice versa.

Response (shape):

```json
{
  "response_context": {
    "correlation_id": "<string>",
    "request_status": "success",
    "time_took_in_seconds": 0
  },
  "total_results": 123,
  "total_matches": 1,
  "matched_prospects": [
    {
      "input": { "email": "[email protected]", "phone_number": null, "linkedin": null, "full_name": null, "company_name": null, "business_id": null },
      "prospect_id": "<md5-like-hash>"
    }
  ]
}
```

Docs source:
- https://developers.explorium.ai/reference/prospects/match_prospects
