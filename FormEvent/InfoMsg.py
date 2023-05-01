from FormEvent import BaseEvent
from FormEvent.BaseWidgetEvent import BaseWidgetEvent



class InfoMsg(BaseWidgetEvent,BaseEvent):

    def __init__(self, _step: int, _body: dict):
        super().__init__()
        self.step = _step
        self.body = _body  
        self.set_style_form_gui()
        self.create_form_gui()

    def closeEvent(self, event):        
        self.play_sound_read()
        self.close()

    def revert_close(self):
        print("revert_close")
        self.revert_hide_event.emit(self.step,self.body)
        
    def postpone_notification(self, delay_minutes):
        self.hide()
        self.send_msg(delay_minutes) 
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_minutes * 60 * 1000, self.showEvent)