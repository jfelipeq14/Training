const Navigation = () => {
  const menuItems = [
    {
      id: 'customers',
      name: 'Clientes',
      icon: 'people',
      description: 'Gestión de clientes',
    },
    {
      id: 'meals',
      name: 'Combos',
      icon: 'restaurant',
      description: 'Gestión de menú y combos',
    },
    {
      id: 'orders',
      name: 'Pedidos',
      icon: 'shopping_cart',
      description: 'Gestión de pedidos',
    },
  ];

  return (
    <nav>
      {menuItems.map(item => (
        <div key={item.id}>
          <span>{item.name}</span>
          <span>{item.description}</span>
        </div>
      ))}
    </nav>
  );
};

export default Navigation;
