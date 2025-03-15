import Button from "@/components/Button"
import formatDate from "@/utils/formatDate"
import { useEffect, useState } from "react"

function HomePage() {
  const [formattedDate, setFormattedDate] = useState<string>()

  useEffect(() => {
    const currentDate = new Date()
    const dateStr = formatDate(currentDate)
    setFormattedDate(dateStr)
  }, [])

  const handleClick = () => {
    alert("Button clicked!")
  }

  return (
    <div>
      <h1>Welcome to the Home Page - {formattedDate}</h1>
      <Button label="Click Me" onClick={handleClick} />
    </div>
  )
}

export default HomePage
