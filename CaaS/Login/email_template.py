import os
import smtplib
import imghdr
from email.message import EmailMessage


def validation_email(reciver_email, otp):

    EMAIL_ADDRESS = "caas.sacumen@gmail.com"
    EMAIL_PASSWORD = 'clarion@123'

    msg = EmailMessage()
    msg['Subject'] = 'CASS One time password for verification...!!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = reciver_email


    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
    <body>
        <table cellspacing="0" border="0" cellpadding="0" width="100%" style="table-layout:fixed;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;background-color:#f7f7f7;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:19px;color:#444;border-collapse:collapse">
            <tbody>
                <tr>
                    <td valign="top" style="padding-top:40px;padding-bottom:40px;background-color:#f7f7f7">
                        <div style="margin-left:auto;margin-right:auto;width:552px;padding-right:15px;padding-left:15px">
                            <table cellspacing="0" border="0" align="center" cellpadding="0" width="552" style="width:552px;text-align:left;border-collapse:collapse">
                                <tbody>
                                    <tr>
                                    <td>
                                        <a href="#"><img style="display:block;border:0;vertical-align:middle;background-color:#f7f7f7;color:#fff;margin-left:auto;margin-right:auto;padding-bottom:40px" src="https://sacumen.com/wp-content/uploads/2019/01/sacumen-logo.png" width="185" height="46" class="CToWUd"></a>
                                    </td>
                                    </tr>
                                    <tr>
                                    <td style="padding-top:50px;padding-bottom:50px;padding-right:50px;padding-left:50px;font-family:Helvetica,Arial,sans-serif;background-color:#ffffff">
                                        <div style="padding-top:0px;padding-bottom:10px;padding-right:10px;font-size:24px;line-height:32px;color:#444">
                                        You're almost there!
                                    </div>
                                    <div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
                                        We just need to verify your email address to complete your registration.
                                    </div>
                                    <div style="padding-top:14px;padding-bottom:28px;padding-right:10px;font-size:14px;line-height:36px;color:#444;text-align:center">

                                        <a href="{otp}" style="color:#fff!important;background-color:#63b246;padding:7px 10px;border-radius:4px;text-decoration:none;display:block;width:200px;height:40px" target="_blank"">Verify Your Email</a>
                                    </div>

                                    <div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
                                    If you have any questions or need help, please visit our <a style="color:#63b246!important" href="#" >support page</a>.
                                    </div>
                                    <div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
                                    </div>
                                    <div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
                                    - Your friends at CAAS 
                                    </div>
                                    </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

    </body>
    </html>

    """.format(otp=otp), subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)  
        return True
    
    return False




import os
import smtplib
import imghdr
from email.message import EmailMessage


def validation_otp(reciver_email, otp):

    EMAIL_ADDRESS = "caas.sacumen@gmail.com"
    EMAIL_PASSWORD = 'clarion@123'

    msg = EmailMessage()
    msg['Subject'] = 'CASS One time password for verification...!!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = reciver_email


    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
    <body>
       <table cellspacing="0" border="0" cellpadding="0" width="100%" style="table-layout:fixed;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;background-color:#f7f7f7;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:19px;color:#444;border-collapse:collapse">
	<tbody>
		<tr>
			<td valign="top" style="padding-top:40px;padding-bottom:40px;background-color:#f7f7f7">
				<div style="margin-left:auto;margin-right:auto;width:552px;padding-right:15px;padding-left:15px">
					<table cellspacing="0" border="0" align="center" cellpadding="0" width="552" style="width:552px;text-align:left;border-collapse:collapse">
						<tbody>
							<tr>
							<td>
								<a href="#"><img style="display:block;border:0;vertical-align:middle;background-color:#f7f7f7;color:#fff;margin-left:auto;margin-right:auto;padding-bottom:40px" src="https://sacumen.com/wp-content/uploads/2019/01/sacumen-logo.png" width="185" height="46" class="CToWUd"></a>
							</td>
							</tr>
							<tr>
							<td style="padding-top:50px;padding-bottom:50px;padding-right:50px;padding-left:50px;font-family:Helvetica,Arial,sans-serif;background-color:#ffffff">
								<div style="padding-top:0px;padding-bottom:10px;padding-right:10px;font-size:24px;line-height:32px;color:#444">
								One Time Password for Verification
							</div>
							<div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
								
							</div>
							<div style="padding-top:14px;padding-bottom:28px;padding-right:10px;font-size:20px;line-height:36px;color:#444;text-align:center">

								<h2>{otp}</h2>
							</div>

							<div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
							If you have any questions or need help, please visit our <a style="color:#63b246!important" href="#" >support page</a>.
							</div>
							<div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
							</div>
							<div style="padding-top:0px;padding-bottom:14px;padding-right:10px;font-size:14px;line-height:19px;color:#444">
							- Your friends at CAAS 
							</div>
							</td>
							</tr>
						</tbody>
					</table>
				</div>
			</td>
		</tr>
	</tbody>
</table>


    </body>
    </html>

    """.format(otp=otp), subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)  
        return True
    
    return False
