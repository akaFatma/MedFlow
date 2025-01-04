import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GrapheComponent } from './graphe.component';

describe('GrapheComponent', () => {
  let component: GrapheComponent;
  let fixture: ComponentFixture<GrapheComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GrapheComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GrapheComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
