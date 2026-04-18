import { useDispatch, useSelector } from 'react-redux';
import { setField } from '../../store/interactionSlice.js';
import TextArea from '../common/TextArea.jsx';
import DatePicker from '../common/DatePicker.jsx';
import './FollowUpSection.css';

function FollowUpSection() {
  const dispatch = useDispatch();
  const { follow_up_notes, follow_up_date } = useSelector((state) => state.interaction);

  return (
    <div className="follow-up-section">
      <TextArea
        label="Follow-up Actions"
        id="follow-up-notes"
        value={follow_up_notes}
        onChange={(e) => dispatch(setField({ field: 'follow_up_notes', value: e.target.value }))}
        placeholder="Describe planned follow-up actions..."
        rows={2}
      />
      <DatePicker
        label="Follow-up Date"
        id="follow-up-date"
        value={follow_up_date}
        onChange={(e) => dispatch(setField({ field: 'follow_up_date', value: e.target.value }))}
      />
    </div>
  );
}

export default FollowUpSection;
