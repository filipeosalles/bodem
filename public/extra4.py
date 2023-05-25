from flask import render_template, session, request, redirect, url_for
import sheet3 as sh3


def main():
    if request.method == 'POST':
        data = session['extra4'] = request.form
        if not session.get('result'):
            return redirect(url_for('home'))
        pf = float(data['pf'])
        oh = sh3.get_oh_by_pF(pf, session['result'])
        session['result_extra4'] = {
            'oh': round(oh, 4),
        }

        return redirect(url_for('extra4'))
    else:
        if not session.get('result_extra4'):
            session['result_extra4'] = {
                'oh': '-',
            }
        if not session.get('extra4'):
            session['extra4'] = {}

        return render_template('extra4.html')
