// qr-scanner.component.ts
import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Input } from '@angular/core';
import { ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { SearchService } from '../../services/search.services'
import { Observable, throwError as observableThrowError } from 'rxjs';
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
  @Output() scanComplete = new EventEmitter<string>();
  @ViewChild('action') action: any;

  constructor(
    private searchService: SearchService,
    private router: Router
  ) {}
  
  show() {
    this.isVisible = true;
  }
  close() {
    this.isVisible = false;
  }


  validateQRCode(qrContent: string): Observable<any> {
    if (!qrContent.startsWith("nss:")) {
      // Handling invalid QR code error
      return this.throwError({ error: 'QR code invalide.', status: 400 });
    }

    const nss = qrContent.split(":")[1];  // Extract the NSS from QR code
    console.log('NSS:', nss);
    return this.searchService.searchByNSS(parseInt(nss))
  }

  onScanSuccess(results: ScannerQRCodeResult[]) {
    if (Array.isArray(results) && results.length > 0) {
      const qrCodeData = results[0]?.value;
      console.log('QR code:', qrCodeData);
      if (this.validateQRCode(qrCodeData)) {
        const nss= parseInt(qrCodeData);     
        this.action.stop();

        this.searchService.searchByNSS(nss).subscribe(
          
          
          
          patient => {
            this.router.navigate(['/dossier-patient',nss]);
          },
          error => {
            console.error('Dossier Patient non trouvé', error);
          }
        );
      }
    }
  }

 trowError(error: { error: string; status: number; }): Observable<any> {
  return observableThrowError(error);
}
throwError(arg0: { error: string; status: number; }): Observable<any> {
  throw new Error('Function not implemented.');
}

}

