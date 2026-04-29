import Button from './Button';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  footer?: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

interface MealCardProps {
  meal: {
    uuid: string;
    name: string;
    category: string;
    description: string;
    price: number;
    available: boolean;
  };
  categoryLabels: Record<string, string>;
  onEdit?: (meal: any) => void;
  onDelete?: (meal: any) => void;
  className?: string;
}

interface StatCardProps {
  title: string;
  value: string | number;
  variant?: 'default' | 'success' | 'warning' | 'danger';
  className?: string;
}

const Card = ({
  children,
  title,
  subtitle,
  footer,
  className = '',
  onClick,
}: CardProps) => {
  return (
    <div className={`card ${className}`} onClick={onClick}>
      {(title || subtitle) && (
        <div className='card-header'>
          {title && <h3 className='card-title'>{title}</h3>}
          {subtitle && <p className='card-subtitle'>{subtitle}</p>}
        </div>
      )}
      <div className='card-body'>{children}</div>
      {footer && <div className='card-footer'>{footer}</div>}
    </div>
  );
};

const MealCard = ({
  meal,
  categoryLabels,
  onEdit,
  onDelete,
  className = '',
}: MealCardProps) => {
  return (
    <Card className={`meal-card ${className}`}>
      <div className='meal-header'>
        <h3 className='meal-name'>{meal.name}</h3>
        <span
          className={`availability ${meal.available ? 'available' : 'unavailable'}`}
        >
          {meal.available ? 'Disponible' : 'No disponible'}
        </span>
      </div>

      <div className='meal-category'>
        <span className='category-badge'>
          {categoryLabels[meal.category] || meal.category}
        </span>
      </div>

      <p className='meal-description'>{meal.description}</p>

      <Card.Footer>
        <span className='price'>${meal.price.toFixed(2)}</span>
        <div className='meal-actions'>
          {onEdit && (
            <Button
              variant='secondary'
              size='sm'
              icon='edit'
              onClick={() => onEdit(meal)}
            >
              Editar
            </Button>
          )}
          {onDelete && (
            <Button
              variant='danger'
              size='sm'
              icon='delete'
              onClick={() => onDelete(meal)}
            >
              Eliminar
            </Button>
          )}
        </div>
      </Card.Footer>
    </Card>
  );
};

const StatCard = ({
  title,
  value,
  variant = 'default',
  className = '',
}: StatCardProps) => {
  return (
    <Card className={`stat-card stat-card-${variant} ${className}`}>
      <div className='stat-content'>
        <h3 className='stat-title'>{title}</h3>
        <span className='stat-value'>{value}</span>
      </div>
    </Card>
  );
};

// Separar el footer como un componente anidado
Card.Footer = ({ children }: { children: React.ReactNode }) => (
  <div className='card-footer'>{children}</div>
);

export { Card, MealCard, StatCard };
export default Card;
