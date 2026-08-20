const INDIA_BOUNDS = {
  minLat: 8,
  maxLat: 30,
  minLng: 68,
  maxLng: 90,
};

function getPosition(latitude, longitude) {
  const x = ((longitude - INDIA_BOUNDS.minLng) / (INDIA_BOUNDS.maxLng - INDIA_BOUNDS.minLng)) * 100;
  const y = 100 - ((latitude - INDIA_BOUNDS.minLat) / (INDIA_BOUNDS.maxLat - INDIA_BOUNDS.minLat)) * 100;
  return { left: `${x}%`, top: `${y}%` };
}

export default function DeliveryMap({ locations }) {
  return (
    <div className="delivery-map">
      <div className="map-surface">
        {locations.slice(0, 30).map((location) => (
          <div
            key={location.order_id}
            className={`map-point status-${location.status.toLowerCase()}`}
            style={getPosition(location.latitude, location.longitude)}
            title={`${location.city} • ${location.status} • Rs ${Math.round(location.amount)}`}
          />
        ))}
      </div>
      <div className="map-legend">
        <span><i className="legend-dot delivered" />Delivered</span>
        <span><i className="legend-dot picked_up" />Picked up</span>
        <span><i className="legend-dot placed" />Placed</span>
        <span><i className="legend-dot cancelled" />Cancelled</span>
      </div>
    </div>
  );
}

