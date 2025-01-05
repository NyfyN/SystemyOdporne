from flask import Flask, request, render_template
from crc_backend import introduce_error, crc_validate, highlight_errors
from crc_backend import highlight_corrected, crc_correct

app = Flask(__name__,  template_folder="/app/templates",
            static_folder="/app/static")
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/crc', methods=['POST'])
def crc():
    data = request.form.get('data')
    poly = request.form.get('poly')

    # Wprowadź błędy i oblicz CRC
    transmitted_data = introduce_error(data, error_rate=0.1)
    errors = crc_validate(transmitted_data, poly)

    # Podświetl błędy w transmisji
    highlighted_message_with_errors = highlight_errors(
        transmitted_data, errors)

    # Naprawa błędów
    crc_corrected = crc_correct(transmitted_data, poly)

    # Podświetlenie błędów po korekcie
    highlighted_message_without_errors = highlight_corrected(
        crc_corrected, errors)

    # Zwróć rezultat
    return render_template('crc.html',
                           data=data,
                           highlighted_message_with_errors=highlighted_message_with_errors,
                           highlighted_message_without_errors=highlighted_message_without_errors,
                           errors=', '.join(map(str, errors)) if errors else 'Brak błędów',
                           crc_corrected=', '.join(map(str, errors)) if crc_corrected else 'Brak błędów')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
