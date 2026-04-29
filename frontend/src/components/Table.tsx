interface TableColumn {
  key: string;
  label: string;
  render?: (value: any, row: any) => React.ReactNode;
  className?: string;
}

interface TableProps {
  data: any[];
  columns: TableColumn[];
  loading?: boolean;
  emptyMessage?: string;
  className?: string;
}

const Table = ({
  data,
  columns,
  loading = false,
  emptyMessage = 'No hay datos disponibles',
  className = '',
}: TableProps) => {
  if (loading) {
    return (
      <div className={`table-container ${className}`}>
        <div className='table-loading'>
          <div className='loading-spinner'></div>
          <span>Cargando...</span>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className={`table-container ${className}`}>
        <div className='table-empty'>
          <span>{emptyMessage}</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`table-container ${className}`}>
      <table className='data-table'>
        <thead>
          <tr>
            {columns.map(column => (
              <th key={column.key} className={column.className}>
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={row.id || row.uuid || index}>
              {columns.map(column => (
                <td key={column.key} className={column.className}>
                  {column.render
                    ? column.render(row[column.key], row)
                    : row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
