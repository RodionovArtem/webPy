"use client"
import { useRouter } from "next/navigation"

export default async function BookPage({params}){
   const id = await params
   

   
   return (<div>
        Book page
    </div>)
}