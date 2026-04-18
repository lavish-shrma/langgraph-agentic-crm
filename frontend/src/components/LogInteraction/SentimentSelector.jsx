import { useDispatch, useSelector } from 'react-redux';
import { setField } from '../../store/interactionSlice.js';
import RadioGroup from '../common/RadioGroup.jsx';
import { SENTIMENT_OPTIONS } from '../../utils/constants.js';

function SentimentSelector() {
  const dispatch = useDispatch();
  const sentiment = useSelector((state) => state.interaction.sentiment);

  return (
    <RadioGroup
      label="Observed HCP Sentiment"
      id="sentiment"
      options={SENTIMENT_OPTIONS}
      value={sentiment}
      onChange={(e) => dispatch(setField({ field: 'sentiment', value: e.target.value }))}
    />
  );
}

export default SentimentSelector;
