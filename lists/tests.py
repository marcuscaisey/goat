class TestHome:
    def test_uses_home_template(self, client):
        response = client.get("/")
        assert "lists/home.html" in (t.name for t in response.templates)

    def test_can_save_POST_request(self, client):
        response = client.post("/", data={"item_text": "A new list item"})
        assert "lists/home.html" in (t.name for t in response.templates)
        assert b"A new list item" in response.content
