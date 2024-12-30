import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NouvelleConsultationComponent } from './nouvelle-consultation.component';

describe('NouvelleConsultationComponent', () => {
  let component: NouvelleConsultationComponent;
  let fixture: ComponentFixture<NouvelleConsultationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NouvelleConsultationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NouvelleConsultationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
