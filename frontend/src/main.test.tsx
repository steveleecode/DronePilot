import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { App } from './App';

describe('DronePilot shell', () => {
  it('renders the viewer foundation', () => {
    render(<App />);

    expect(screen.getByLabelText('Drone CAD viewer')).toBeInTheDocument();
  });
});
