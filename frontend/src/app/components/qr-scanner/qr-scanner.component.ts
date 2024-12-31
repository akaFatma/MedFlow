import { Component, OnInit } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ZXingScannerModule } from '@zxing/ngx-scanner';
import { BarcodeFormat } from '@zxing/library';

@Component({
  imports: [BrowserModule, ZXingScannerModule],
  templateUrl: './qr-scanner.component.html',
  styleUrls: ['./qr-scanner.component.scss']
})
export class QrScannerComponent implements OnInit {
  formats: BarcodeFormat[] = [BarcodeFormat.QR_CODE]; // Already in use for formats
  BarcodeFormat = BarcodeFormat; // Expose BarcodeFormat to the template
  scanResult: string | null = null;
  availableDevices: MediaDeviceInfo[] = [];
  selectedDevice: MediaDeviceInfo | null = null;
  hasTorch = false;

  constructor() {}

  ngOnInit(): void {}

  onScanSuccess(result: string): void {
    this.scanResult = result;
    console.log('Scanned QR code:', result);
  }

  onCamerasFound(devices: MediaDeviceInfo[]): void {
    this.availableDevices = devices;
    if (devices.length > 0) {
      this.selectedDevice = devices[0]; // Select the first camera by default
      this.hasTorch = this.selectedDevice && 'torch' in this.selectedDevice;
    }
  }

  onCamerasNotFound(): void {
    console.error('No cameras found.');
  }

  handleError(error: any): void {
    console.error('Error during scan:', error);
  }

  onDeviceSelect(event: Event): void {
    const target = event.target as HTMLSelectElement;
    const deviceId = target.value;
    this.selectedDevice = this.availableDevices.find(device => device.deviceId === deviceId) || null;
  }
}
