import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LoginComponent } from './components/auth-card/auth-card.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,LoginComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  template : `<app-login></app-login>`,
})
export class AppComponent {
  title = 'gestionDPI';

}
