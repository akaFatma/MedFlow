// qr-scanner.component.ts
import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Input } from '@angular/core';
import { ViewChild } from '@angular/core';
import {
  NgxScannerQrcodeModule,
  LOAD_WASM,
  ScannerQRCodeResult,
} from 'ngx-scanner-qrcode';

@Component({
  selector: 'app-qr-scanner',
  standalone: true,
  imports: [NgxScannerQrcodeModule, CommonModule, FormsModule],
  providers: [
    {
      provide: LOAD_WASM,
      useValue: 'assets/wasm/ngx-scanner-qrcode.wasm',
    },
  ],
  templateUrl: './qr-scanner.component.html',
  styleUrls: ['./qr-scanner.component.scss']
})
export class QrScannerComponent {
  @Input() isVisible = false;
  @Output() closePopup = new EventEmitter<void>();
  @ViewChild('action') action: any;
  
  show() {
    this.isVisible = true;
  }
  close() {
    this.isVisible = false;
  }


  onScanSuccess(results: ScannerQRCodeResult[]) {
    if (Array.isArray(results) && results.length > 0) {
      const qrCodeData = results[0]?.value;
    }
  }
}
