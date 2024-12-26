import { Component } from '@angular/core';

interface Alert {
  title: string;
  description: string;
  isVisible?: boolean;
}

@Component({
  selector: 'app-success-notif',
  imports: [],
  templateUrl: './success-notif.component.html',
  styleUrl: './success-notif.component.scss'
})
export class SuccessNotifComponent {

  alert: Alert | null = null;

  showAlert(title: string, description: string) {
    this.alert = {
      title: title,
      description: description,
      isVisible: true
    };
    
    setTimeout(() => {
      this.hideAlert();
    }, 5000);
  }
  hideAlert() {
    this.alert = null;
  }

  onActionSuccess() {
    this.showAlert('done successfully :)', 'This is the description section');
  }
}





}
