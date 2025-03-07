import logo from '../pictures/logo.png'

interface Props{
  size?: number;
}

function BotIcon({size=50}: Props) {
  return (
    <div><img className='bot-image' src={logo} alt="bot" width={size} /></div>
  )
}

export default BotIcon