import { ButtonHTMLAttributes, forwardRef } from 'react';
import clsx from 'clsx';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', loading, children, className, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={clsx(
          'inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition-colors',
          'focus:outline-none focus:ring-2 focus:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-60',
          {
            'bg-brand-600 text-white hover:bg-brand-700 focus:ring-brand-500': variant === 'primary',
            'bg-white text-gray-700 ring-1 ring-gray-300 hover:bg-gray-50 focus:ring-brand-500':
              variant === 'secondary',
            'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500': variant === 'danger',
          },
          className
        )}
        {...props}
      >
        {loading ? 'Yuklanmoqda...' : children}
      </button>
    );
  }
);

Button.displayName = 'Button';
