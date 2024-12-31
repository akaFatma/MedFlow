// qr-scanner.component.ts
import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  NgxScannerQrcodeModule,
  NgxScannerQrcodeService,
  ScannerQRCodeResult,
  ScannerQRCodeConfig,
  NgxScannerQrcodeComponent
} from 'ngx-scanner-qrcode';

@Component({
  selector: 'app-qr-scanner',
  standalone: true,
  imports: [
    CommonModule,
    NgxScannerQrcodeModule
  ],
  templateUrl: './qr-scanner.component.html',
  styleUrls: ['./qr-scanner.component.scss'],
  providers: [NgxScannerQrcodeService]
})
export class QrScannerComponent implements OnInit, OnDestroy {
  @ViewChild('action') action!: NgxScannerQrcodeComponent;
  
  public isFrontCamera = false;
  
  public config: ScannerQRCodeConfig = {
    constraints: {
      video: {
        width: 640,
        height: 480,
        facingMode: "environment"  // Start with back camera
      }
    },
    canvasStyles: {
      width: '100%'
    } as any
  };

  public qrResult: string = '';

  constructor(private qrService: NgxScannerQrcodeService) {}

  ngOnInit(): void {}

  ngOnDestroy(): void {
    this.action.stop();
  }

  onEvent(e: ScannerQRCodeResult[]): void {
    if (e && e.length > 0) {
      this.qrResult = e[0].value;
    }
  }

  async switchCamera(): Promise<void> {
    // Stop the current stream
    await this.action.stop();
    
    // Toggle camera mode
    this.isFrontCamera = !this.isFrontCamera;
    
    // Update config with new facing mode
    this.config = {
      ...this.config,
      constraints: {
        video: {
          width: 640,
          height: 480,
          facingMode: this.isFrontCamera ? "user" : "environment"
        }
      }
    };
    
    // Restart the scanner with new config
    await this.action.start();
  }
}