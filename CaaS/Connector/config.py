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

solarwinds_payload = {
    "incident": {
        "priority": "Critical",
        "requester": {}
    }

}

hubspot_payload = [
    {
        "name": "subject"    
    },
    {
        "name": "content"
    },
    {
        "name": "hs_pipeline",
        "value": "0"
    },
    {
        "name": "hs_pipeline_stage",
        "value": "1"
    }
]

agilecrm_payload = {
    "requester_name": "Deepak Baraik",
    "requester_email": "deepak.baraik@sacumen.com",
    "subject": "Test not working ??",
    "priority": "LOW",
    "status": "OPEN",
    "groupID": "5756098678095872",
    "html_text": "Hello I am testing your docs and find that Test is not working. Please help me",
    "cc_emails": [
        "tester@gmail.com"
    ],
    "labels": None
}