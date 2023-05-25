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
        data = session['extra2'] = request.form
        if not session.get('result'):
            return redirect(url_for('home'))
        mwhc = data['mwhc']
        mwhc_fraction = float(mwhc) / 100
        rho_default = 1.5
        rho_act = float(data['mwhc_density'])
        session['rho_act'] = rho_act
        mwhc_vv = (mwhc_fraction * rho_default if rho_act == 0 else mwhc_fraction * rho_act) if data[
                                                                                                    'type_mwhc'] == 'w/w' else mwhc_fraction
        pf_mwhc_value = int(data['pf_mwhc'])
        correction_factor_MWHC = sh3.get_soil_type_by_pf(pf_mwhc_value, session['result'])
        if pf_mwhc_value == 0:
            correction_factor_MWHC = 1
        else:
            correction_factor_MWHC = sh3.get_soil_type_by_pf(0, session['result']) / correction_factor_MWHC

        MWHC_vv_at_pF0 = mwhc_vv * round(correction_factor_MWHC, 4)
        oact = MWHC_vv_at_pF0 * (float(data['percent_mwhc']) / 100)
        pF_at_θact = sh3.get_pf_at_oact(round(oact, 6), session['result'])
        session['result_extra2'] = {
            'correction_factor_MWHC': round(correction_factor_MWHC, 4),
            'MWHC_vv_at_pF0': round(MWHC_vv_at_pF0, 4),
            'oact': round(oact, 4),
            'pF_at_θact': pF_at_θact,
        }

        return redirect(url_for('extra2'))
    else:
        if not session.get('result_extra2'):
            session['result_extra'] = {
                'correction_factor_MWHC': '-',
                'MWHC_vv_at_pF0': '-',
                'oact':'-',
                'pF_at_θact': '-',
            }
        if not session.get('extra2'):
            session['extra2'] = {}

        return render_template('extra2.html', data={'type_mwhc': type_mwhc, 'pf_mwhc': pf_mwhc})
