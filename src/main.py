from flask import Flask, request, render_template
from CRC import CRC
from utils import word_to_binary, binary_to_word, highlight_corrected, highlight_errors
app = Flask(__name__,  template_folder="/app/templates",
            static_folder="/app/static")
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/crc', methods=['POST'])
def crc():
    data = request.form.get('data')
    key = request.form.get('poly')
    
    # Create a CRC object
    crc = CRC()
    
    # Convert the input data to binary
    binary_data = word_to_binary(data)
    
    # Encode the binary data using the provided key
    crc.encodedData(binary_data, key)
    
    # Introduce errors into the encoded data
    error_data, error_positions = crc.introduceError(crc.cdw)
    
    # Convert the error data back to a string
    error_string_data = binary_to_word(error_data).encode('utf-8').decode('utf-8')
    
    # Highlight the errors in the message
    highlighted_message_with_errors = highlight_errors(error_data, error_positions)
    
    # Get the message without errors
    message_without_errors = crc.cdw
    
    # Highlight the corrected message
    highlighted_message_without_errors = highlight_corrected(message_without_errors, error_positions)
    
    # Convert the corrected message back to a string
    string_message_without_errors = binary_to_word(crc.cdw).encode('utf-8').decode('utf-8')
    
    # Adjust the length of the corrected message to match the original data length
    diff = len(data) - len(string_message_without_errors)
    string_message_without_errors = string_message_without_errors[:diff]
    
    # Prepare the error positions for display
    errors = ', '.join(map(str, sorted(error_positions)))
    if len(errors) == 0:
        errors = "Brak"
    
    # Return result
    return render_template('crc.html',
                           data=data,
                           highlighted_message_with_errors=highlighted_message_with_errors,
                           error_string_data=error_string_data,
                           highlighted_message_without_errors=highlighted_message_without_errors,
                           string_message_without_errors=string_message_without_errors,
                           errors=errors,
                           crc_corrected=errors)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
