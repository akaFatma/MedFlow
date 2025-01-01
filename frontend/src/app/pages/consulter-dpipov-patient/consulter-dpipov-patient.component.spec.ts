import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsulterDPIPovPatientComponent } from './consulter-dpipov-patient.component';

describe('ConsulterDPIPovPatientComponent', () => {
  let component: ConsulterDPIPovPatientComponent;
  let fixture: ComponentFixture<ConsulterDPIPovPatientComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsulterDPIPovPatientComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsulterDPIPovPatientComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
