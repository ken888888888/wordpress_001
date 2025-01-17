from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            target_age = int(request.form['target_age'])
            current_age = int(request.form['current_age'])

            # 入力値が無効な場合
            if target_age <= current_age:
                error_message = "目標年齢は現在の年齢より大きい値を入力してください。"
                return render_template_string(index_html, error_message=error_message)

            # 残り年数、月数、日数を計算
            remaining_years = target_age - current_age
            remaining_months = remaining_years * 12  # 年数を月数に変換

            # より正確な日数計算（閏年を考慮）
            remaining_days = remaining_years * 365.25  # 1年を365.25日として計算

            # 結果を表示
            return render_template_string(result_html, remaining_years=remaining_years, remaining_days=int(remaining_days), remaining_months=remaining_months)
        except ValueError:
            # 入力が整数でない場合のエラーハンドリング
            error_message = "年齢は整数を入力してください。"
            return render_template_string(index_html, error_message=error_message)
    else:
        return render_template_string(index_html)

# HTMLテンプレートの定義（index.html）
index_html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>年齢計算</title>
    <style>
        body {
            font-family: 'Meiryo', sans-serif;
            color: #222222;
            font-size: 15px;
        }
        input[type="number"] {
            font-family: 'Meiryo', sans-serif;
            font-size: 15px;
        }
        form {
            margin-top: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type="submit"] {
            margin-top: 20px;
            font-size: 15px;
        }
        .error-message {
            color: red;
        }
        .heading {
            font-size: 15px;
            font-weight: normal;
        }
    </style>
</head>
<body>
    <p class="heading">〖 目標年齢までの残り期間を計算 〗</p>

    {% if error_message %}
        <p class="error-message">{{ error_message }}</p>
    {% endif %}

    <form method="POST">
        <label for="target_age">何歳まで生きたいですか？</label>
        <input type="number" id="target_age" name="target_age" required> 歳<br>

        <label for="current_age">現在の年齢は何歳ですか？</label>
        <input type="number" id="current_age" name="current_age" required> 歳<br>

        <input type="submit" value="計算">
    </form>
</body>
</html>
"""

# 結果表示用のHTMLテンプレート（result.html）
result_html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>計算結果</title>
    <style>
        body {
            font-family: 'Meiryo', sans-serif;
            color: #222222;
            font-size: 15px;
        }
        .heading {
            font-size: 15px;
            font-weight: normal;
        }
    </style>
</head>
<body>
    <p class="heading">〖 計算結果 〗</p>
    <p>残りは約{{ remaining_years }}年です。</p>
    <p>または、約{{ remaining_months }}ヶ月です。</p>
    <p>または、約{{ remaining_days }}日です。</p>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
