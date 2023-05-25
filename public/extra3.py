from flask import render_template, session, request, redirect, url_for
import sheet3 as sh3

type_mwhc = [
    {'id': 'v/v', 'name': 'V/V'},
    {'id': 'w/w', 'name': 'W/W'},
]

pf_mwhc = [
    {'id': '0', 'name': 'pF 0'},
    {'id': '1', 'name': 'pF 1'},
    {'id': '2', 'name': 'pF 2'},
]


def main():
    if request.method == 'POST':
        data = session['extra3'] = request.form
        if not session.get('result'):
            return redirect(url_for('home'))
        field_capacity = float(data['field_capacity'])
        mwhc_fraction = field_capacity / 100
        rho_default = 1.5
        rho_act = session.get('rho_act') or 0
        ofc_act_v_v = (mwhc_fraction * rho_default if rho_act == 0 else mwhc_fraction * rho_act) if data[
                                                                                                    'type_mwhc'] == 'w/w' else mwhc_fraction
        ofc_act_75 = ofc_act_v_v * 0.75
        pF_at_75_act = sh3.get_pf_at_oact(round(ofc_act_75, 4), session['result'])
        session['result_extra3'] = {
            'ofc_act_v_v': round(ofc_act_v_v, 4),
            'ofc_act_75': round(ofc_act_75, 4),
            'pF_at_75_θact': pF_at_75_act,
        }

        return redirect(url_for('extra3'))
    else:
        if not session.get('result_extra3'):
            session['result_extra3'] = {
                'ofc_act_v_v': '-',
                'ofc_act_75': '-',
                'pF_at_75_θact': '-',
            }
        if not session.get('extra3'):
            session['extra3'] = {}

        return render_template('extra3.html', data={'type_mwhc': type_mwhc, 'pf_mwhc': pf_mwhc})
