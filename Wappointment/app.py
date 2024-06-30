import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Klasör yolları
TEMPLATES_FOLDER = os.path.join(os.getcwd(), 'templates')
USER_APPOINTMENT_FOLDER = os.path.join(TEMPLATES_FOLDER, 'userAppointmentFiles')
USER_DATA_FOLDER = os.path.join(TEMPLATES_FOLDER, 'userDatas')
EXCEL_PATH = os.path.join(USER_DATA_FOLDER, 'userData.xlsx')
EXCEL_PATH2 = ''
# Eğer userAppointmentFiles klasörü yoksa oluştur
if not os.path.exists(USER_APPOINTMENT_FOLDER):
    os.makedirs(USER_APPOINTMENT_FOLDER)

# Eğer userDatas klasörü yoksa oluştur
if not os.path.exists(USER_DATA_FOLDER):
    os.makedirs(USER_DATA_FOLDER)

def get_user_appointment_file(username):
    """Kullanıcı adına göre randevu dosyasının yolunu döndürür."""
    return os.path.join(USER_APPOINTMENT_FOLDER, f"{username}.xlsx")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global EXCEL_PATH2
    username = request.form['username']
    password = request.form['password']
    
    user_data_path = os.path.join(USER_DATA_FOLDER, 'userData.xlsx')
    if os.path.exists(user_data_path):
        user_data = pd.read_excel(user_data_path)
    else:
        flash('Giriş yapmak için kullanıcı kaydı bulunamadı.', 'error')
        return redirect(url_for('index'))
    
    if username in user_data['username'].values:
        user = user_data[user_data['username'] == username].iloc[0]
        if password == user['password']:
            session['logged_in'] = True
            session['username'] = username
            EXCEL_PATH2 = 'templates/userAppointmentFiles/' + username + '.xlsx'  # Excel dosya yolunu burada belirleyin
            
            return redirect(url_for('welcome'))
    
    flash('Geçersiz kullanıcı adı veya şifre', 'error')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if ' ' in username:
            flash('Kullanıcı adı boşluk içeremez!', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Şifreler eşleşmiyor!', 'error')
            return redirect(url_for('register'))
        
        user_data_path = os.path.join(USER_DATA_FOLDER, 'userData.xlsx')
        if os.path.exists(user_data_path):
            user_data = pd.read_excel(user_data_path)
        else:
            user_data = pd.DataFrame(columns=['username', 'email', 'password'])
        
        if username in user_data['username'].values:
            flash('Bu kullanıcı adı zaten alınmış.', 'error')
            return redirect(url_for('register'))
        
        if email in user_data['email'].values:
            flash('Bu e-posta adresi zaten kayıtlı.', 'error')
            return redirect(url_for('register'))
        
        new_user = pd.DataFrame({'username': [username], 'email': [email], 'password': [password]})
        user_data = pd.concat([user_data, new_user], ignore_index=True)
        
        try:
            user_data.to_excel(user_data_path, index=False)
        except Exception as e:
            flash(f'Kullanıcı verileri kaydedilirken bir hata oluştu: {str(e)}', 'error')
            return redirect(url_for('register'))
        
        # Yeni Excel dosyasını oluştur
        user_excel_path = get_user_appointment_file(username)
        user_df = pd.DataFrame(columns=['Tarih', 'İsim'])
        
        try:
            user_df.to_excel(user_excel_path, index=False)
        except Exception as e:
            flash(f'Randevu dosyası oluşturulurken bir hata oluştu: {str(e)}', 'error')
            # Hata durumunda kullanıcı veri tabanından silinebilir
            user_data = user_data[user_data['username'] != username]
            user_data.to_excel(user_data_path, index=False)
            return redirect(url_for('register'))
        
        flash('Başarıyla kayıt oldunuz! Lütfen giriş yapınız.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'logged_in' in session and session['logged_in']:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/randevular', methods=['GET', 'POST'])
def randevular():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            Tarih = request.form.getlist('Tarih')
            İsim = request.form.getlist('İsim')

            # Verileri Excel dosyasına kaydet
            df = pd.DataFrame({'Tarih': Tarih, 'İsim': İsim})
            df.to_excel(EXCEL_PATH2, index=False)

        # Excel dosyasını oku
        if os.path.exists(EXCEL_PATH2):
            df = pd.read_excel(EXCEL_PATH2)
            data = df.to_dict(orient='list')
        else:
            data = {'Tarih': [], 'İsim': []}

        return render_template('randevular.html', data=data)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
