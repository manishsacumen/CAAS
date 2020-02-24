payload = {
                "fields": {
                    "project":
                        {
                            "key": "FIR"
                        },
                    "summary": "New Issue is created on {}.",
                    "description": {
                        "version": 1,
                        "type": "doc",
                        "content": [
                            {"type": "paragraph", "content":
                                [{"type": "text", "text": 'Sample'}]
                             }
                        ]
                    },
                    "issuetype": {
                        "name": "Bug"
                    }
                }
            }
servicenow_payload = {
    "short_description":"Test incident creation through REST", 
    "comments":"These are my comments"}