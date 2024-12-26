import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MedecinLandingPageComponent } from './medecin-landing-page.component';

describe('MedecinLandingPageComponent', () => {
  let component: MedecinLandingPageComponent;
  let fixture: ComponentFixture<MedecinLandingPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MedecinLandingPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MedecinLandingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
