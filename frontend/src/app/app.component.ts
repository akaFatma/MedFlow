import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NgxScannerQrcodeModule, LOAD_WASM } from 'ngx-scanner-qrcode';
import { SignOutButtonComponent } from './components/sign-out-button/sign-out-button.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  standalone: true,
  imports: [
    RouterOutlet,
    CommonModule,
    NgxScannerQrcodeModule,
    SignOutButtonComponent,
  ],
})
export class AppComponent {
  title = 'gestionDPI';

  constructor(private router: Router) {}
}
