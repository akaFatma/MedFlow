import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SuccessNotifComponent } from './success-notif.component';

describe('SuccessNotifComponent', () => {
  let component: SuccessNotifComponent;
  let fixture: ComponentFixture<SuccessNotifComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SuccessNotifComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SuccessNotifComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
