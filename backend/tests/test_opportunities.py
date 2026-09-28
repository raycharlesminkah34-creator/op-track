import pytest


def test_create_opportunity_minimal(client):
    payload = {
        "title": "Software Engineer Intern",
        "organization": "Google",
        "opportunity_type": "internship",
    }
    response = client.post("/api/v1/opportunities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == "Software Engineer Intern"
    assert data["organization"] == "Google"
    assert data["opportunity_type"] == "internship"
    assert data["status"] == "discovered"
    assert data["deadline"] is None
    assert data["url"] is None
    assert data["notes"] is None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_create_opportunity_all_fields(client):
    payload = {
        "title": "PhD in Computer Science",
        "organization": "MIT",
        "opportunity_type": "graduate_program",
        "status": "applying",
        "deadline": "2026-12-15",
        "url": "https://mit.edu/cs-phd",
        "notes": "Requires 3 recommendation letters.",
    }
    response = client.post("/api/v1/opportunities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "PhD in Computer Science"
    assert data["organization"] == "MIT"
    assert data["opportunity_type"] == "graduate_program"
    assert data["status"] == "applying"
    assert data["deadline"] == "2026-12-15"
    assert data["url"] == "https://mit.edu/cs-phd"
    assert data["notes"] == "Requires 3 recommendation letters."


def test_create_opportunity_missing_required_fields(client):
    # Missing organization and opportunity_type
    response = client.post(
        "/api/v1/opportunities",
        json={"title": "Data Scientist"},
    )
    assert response.status_code == 422


def test_create_opportunity_invalid_type(client):
    payload = {
        "title": "Research Grant",
        "organization": "NSF",
        "opportunity_type": "grant",  # Invalid type
    }
    response = client.post("/api/v1/opportunities", json=payload)
    assert response.status_code == 422


def test_create_opportunity_invalid_status(client):
    payload = {
        "title": "Frontend Engineer",
        "organization": "Acme",
        "opportunity_type": "job",
        "status": "pending_review",  # Invalid status
    }
    response = client.post("/api/v1/opportunities", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "status_val",
    [
        "discovered",
        "saved",
        "applying",
        "applied",
        "interviewing",
        "offered",
        "rejected",
        "withdrawn",
    ],
)
def test_all_valid_statuses_supported(client, status_val):
    payload = {
        "title": f"Opportunity with {status_val}",
        "organization": "Test Corp",
        "opportunity_type": "job",
        "status": status_val,
    }
    response = client.post("/api/v1/opportunities", json=payload)
    assert response.status_code == 201
    assert response.json()["status"] == status_val


def test_get_opportunities_empty(client):
    response = client.get("/api/v1/opportunities")
    assert response.status_code == 200
    assert response.json() == []


def test_get_opportunities_list(client):
    for i in range(3):
        client.post(
            "/api/v1/opportunities",
            json={
                "title": f"Job {i}",
                "organization": f"Org {i}",
                "opportunity_type": "job",
            },
        )

    response = client.get("/api/v1/opportunities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_get_opportunities_filter_by_status(client):
    client.post(
        "/api/v1/opportunities",
        json={"title": "Opp 1", "organization": "Org 1", "opportunity_type": "job", "status": "saved"},
    )
    client.post(
        "/api/v1/opportunities",
        json={"title": "Opp 2", "organization": "Org 2", "opportunity_type": "job", "status": "applied"},
    )

    response = client.get("/api/v1/opportunities?status=applied")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["status"] == "applied"
    assert results[0]["title"] == "Opp 2"


def test_get_opportunities_filter_by_type(client):
    client.post(
        "/api/v1/opportunities",
        json={"title": "Opp 1", "organization": "Org 1", "opportunity_type": "job"},
    )
    client.post(
        "/api/v1/opportunities",
        json={"title": "Opp 2", "organization": "Org 2", "opportunity_type": "scholarship"},
    )

    response = client.get("/api/v1/opportunities?opportunity_type=scholarship")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["opportunity_type"] == "scholarship"


def test_get_opportunities_search(client):
    client.post(
        "/api/v1/opportunities",
        json={"title": "Backend Python Developer", "organization": "Stripe", "opportunity_type": "job"},
    )
    client.post(
        "/api/v1/opportunities",
        json={"title": "Frontend React Engineer", "organization": "Vercel", "opportunity_type": "job"},
    )

    response = client.get("/api/v1/opportunities?search=stripe")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["organization"] == "Stripe"


def test_get_opportunity_by_id_success(client):
    create_res = client.post(
        "/api/v1/opportunities",
        json={"title": "ML Engineer", "organization": "DeepMind", "opportunity_type": "job"},
    )
    opp_id = create_res.json()["id"]

    get_res = client.get(f"/api/v1/opportunities/{opp_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["id"] == opp_id
    assert data["title"] == "ML Engineer"
    assert data["organization"] == "DeepMind"


def test_get_opportunity_by_id_not_found(client):
    response = client.get("/api/v1/opportunities/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_patch_opportunity_partial(client):
    create_res = client.post(
        "/api/v1/opportunities",
        json={
            "title": "Staff Engineer",
            "organization": "OpenAI",
            "opportunity_type": "job",
            "status": "applied",
        },
    )
    opp_id = create_res.json()["id"]

    patch_res = client.patch(
        f"/api/v1/opportunities/{opp_id}",
        json={"status": "interviewing"},
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated["status"] == "interviewing"
    assert updated["title"] == "Staff Engineer"  # untouched


def test_patch_opportunity_multiple_fields(client):
    create_res = client.post(
        "/api/v1/opportunities",
        json={"title": "Dev", "organization": "Meta", "opportunity_type": "job"},
    )
    opp_id = create_res.json()["id"]

    patch_res = client.patch(
        f"/api/v1/opportunities/{opp_id}",
        json={
            "title": "Senior Dev",
            "notes": "Referred by John",
            "deadline": "2026-11-01",
        },
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated["title"] == "Senior Dev"
    assert updated["notes"] == "Referred by John"
    assert updated["deadline"] == "2026-11-01"


def test_patch_opportunity_invalid_status(client):
    create_res = client.post(
        "/api/v1/opportunities",
        json={"title": "Dev", "organization": "Meta", "opportunity_type": "job"},
    )
    opp_id = create_res.json()["id"]

    patch_res = client.patch(
        f"/api/v1/opportunities/{opp_id}",
        json={"status": "not_a_valid_status"},
    )
    assert patch_res.status_code == 422


def test_patch_opportunity_not_found(client):
    response = client.patch(
        "/api/v1/opportunities/99999",
        json={"title": "New Title"},
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_opportunity_success(client):
    create_res = client.post(
        "/api/v1/opportunities",
        json={"title": "To Delete", "organization": "Test Org", "opportunity_type": "job"},
    )
    opp_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/opportunities/{opp_id}")
    assert del_res.status_code == 204

    # Subsequent GET should return 404
    get_res = client.get(f"/api/v1/opportunities/{opp_id}")
    assert get_res.status_code == 404


def test_delete_opportunity_not_found(client):
    response = client.delete("/api/v1/opportunities/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
