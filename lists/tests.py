class TestHome:
    def test_uses_home_template(self, client):
        response = client.get("/")
        assert "lists/home.html" in (t.name for t in response.templates)
