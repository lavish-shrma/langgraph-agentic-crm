import { useDispatch, useSelector } from 'react-redux';
import { setField } from '../../store/interactionSlice.js';
import Button from '../common/Button.jsx';
import './SampleEntry.css';

function SampleEntry() {
  const dispatch = useDispatch();
  const samples = useSelector((state) => state.interaction.samples);

  const addSample = () => {
    dispatch(setField({
      field: 'samples',
      value: [...samples, { product_name: '', quantity: 1 }],
    }));
  };

  const removeSample = (index) => {
    const updated = samples.filter((_, i) => i !== index);
    dispatch(setField({ field: 'samples', value: updated }));
  };

  const updateSample = (index, field, value) => {
    const updated = samples.map((s, i) =>
      i === index ? { ...s, [field]: value } : s
    );
    dispatch(setField({ field: 'samples', value: updated }));
  };

  return (
    <div className="sample-entry">
      <div className="sample-entry__header">
        <label className="input-label">Samples Distributed</label>
        <Button variant="ghost" size="sm" onClick={addSample} id="add-sample-btn">
          + Add Sample
        </Button>
      </div>

      {samples.length > 0 && (
        <div className="sample-entry__list">
          {samples.map((sample, index) => (
            <div key={index} className="sample-entry__row animate-fade-in">
              <input
                type="text"
                value={sample.product_name}
                onChange={(e) => updateSample(index, 'product_name', e.target.value)}
                placeholder="Product name"
                className="sample-entry__input sample-entry__input--name"
              />
              <input
                type="number"
                value={sample.quantity}
                onChange={(e) => updateSample(index, 'quantity', parseInt(e.target.value, 10) || 1)}
                placeholder="Qty"
                min="1"
                className="sample-entry__input sample-entry__input--qty"
              />
              <button
                className="sample-entry__remove"
                onClick={() => removeSample(index)}
                title="Remove sample"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      {samples.length === 0 && (
        <p className="sample-entry__empty">No samples added yet</p>
      )}
    </div>
  );
}

export default SampleEntry;
