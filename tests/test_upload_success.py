def test_upload_success(client):
    with open("tests/resources/sample.jpeg", "rb") as f:
        response = client.post(
            "/files", files={"file": ("sample.jpeg", f, "image/jpeg")}
        )

        status_code = response.status_code
        data = response.json()

        assert status_code == 201, f"Expected status code 201, got {status_code}"
        assert data["original_filename"] == "sample.jpeg"
        assert data["content_type"] == "image/jpeg"
        assert data["size"] > 0
        assert data["id"] is not None
