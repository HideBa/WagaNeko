
<!-- 以下問題 -->
<!-- <p>この本を評価してください。</p>
<form action="{% url 'waganeko:book_rate' book_id=book.id %}" method="POST">
    {% csrf_token %}
    {% if current_score >= 0 %}
    <input type="number" name="score" min="1" max="5" value="{{ current_score }}" required />
    {% else %}
    <input type="number" name="score" min="1" max="5" required />
    {% endif %}
    <input type="submit" name="submit" value="送信" />
</form> -->