import { Component } from '@angular/core';
import { Input } from '@angular/core';

interface Alert {
  title: string;
  description: string;
  isVisible?: boolean;
}

@Component({
  selector: 'app-success-notif',
  imports: [],
  standalone : true,
  templateUrl: './success-notif.component.html',
  styleUrl: './success-notif.component.scss'
})
export class SuccessNotifComponent {
  @Input() isVisible: boolean = false;
   @Input() title: string = '';         // Bindable input for the title
  @Input() description: string = ''; 

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






