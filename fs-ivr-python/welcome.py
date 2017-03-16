import freeswitch

def handler(session, args):
    session.answer()

    while session.ready() == True:
        session.setAutoHangup(False)
        session.set_tts_params("flite", "slt")
        session.speak("Welcome to A T L InfoTech!")
        session.sleep(100)
        session.speak("please select an Action.")
        session.sleep(100)
        session.speak("press 1, to listen Voice Mail")
        session.sleep(100)
        session.speak("press 2, to call Freeswitch I V R")
        session.sleep(100)
        session.speak("press 3, for Music on hold")
        session.sleep(100)
        session.speak("press 4, to call Jamal Shahverdiev")
        session.sleep(100)
        session.speak("press 5, to call Ayaz Gulmammadov")
        session.sleep(3000)
        digits = session.getDigits(1, "", 3000)

        if digits == "1":
            session.setAutoHangup(False)
            session.set_tts_params("flite", "slt")
            session.speak("Welcome to RISK company!")
            session.sleep(100)
            session.speak("please select an Action.")
            session.sleep(100)
            session.speak("Call to your extension")
            session.sleep(100)
            session.speak("Or wait answer from operator!")
            session.sleep(4000)
            nums = session.getDigits(4, "", 4000)

            if nums == "1006":
                session.execute("execute_extension", "1006 XML default")

        if digits == "2":
            session.execute("transfer","5000")
        if digits == "3":
            session.execute("transfer","9999")
        if digits == "4":
            session.execute("execute_extension", "1002 XML default")
        if digits == "5":
            session.execute("execute_extension", "1006 XML default")

