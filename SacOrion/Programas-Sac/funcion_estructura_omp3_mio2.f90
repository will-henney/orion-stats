program  funcion_estructura_omp3_mio
  ! calculates the emissivity cube in a given line from the                     
  ! datacubes of density, ionization fraction, temperature                      
  use wfitsutils, only: fitsread, fitswrite, fitsimage 
!fitscube
 
! use emissmod, only: emtype, emissivity 
  implicit none 
  character(len=100)::archivos
  real, dimension(:,:), allocatable :: Vc
  real, dimension(:),allocatable::suma
  integer, dimension(:),allocatable::num
  character(len=15) :: emtype 
  integer ::i,j,ii,jj, nx, ny,nx1,nx2,ny1,ny2,komp,np, npts
  integer, save :: i1,i2,j1,j2, l1,l2,l
  real, save::pix,piy,dd,lmin,lmax, pi,pj
!$OMP THREADPRIVATE(i1,i2,j1,j2,l1,l2,l,pix,piy,dd,lmin,lmax, pi,pj)
  real, parameter:: valmin=0.000001
  real :: sumv, varvc, promvc,v1,v2

  !print *, 'File prefix?' 
  !read '(a)', prefix 
  print *, 'Emissivity type?' 
  read '(a)', emtype

!num arreglo
!caracter ftag

  print*,'filename ', trim(emtype)//'_-040+070.wisomom-mean-smooth2d.fits'
  call fitsread(trim(emtype)//'_-040+070.wisomom-mean-smooth2d.fits')
  nx = size(fitsimage, 1) 
  ny = size(fitsimage, 2)

print*, 'nx', nx, 'ny', ny

nx1=2
nx2=nx-2
ny1=100
ny2=ny-100

print*, 'nx2', nx2,'ny2', ny2
  
 allocate( Vc(nx2, ny2) ) 
  Vc=fitsimage


  allocate(suma(nx2),num(nx2))

  num=0
  suma=0.0


  deallocate(fitsimage)          ! Free up unneeded memory                    

v1=-50.0
v2=100.0

sumv = 0.0
npts = 0
 do i=nx1,nx2
     do j=ny1,ny2
      if(Vc(i,j)>v1.and.Vc(i,j)<v2) then
         sumv = sumv + Vc(i,j)
         npts = npts + 1
      endif
   end do
end do
promvc = sumv/real(npts)
sumv = 0.0
npts = 0
 do i=nx1, nx2
     do j=ny1,ny2
      if(Vc(i,j)>v1.and.Vc(i,j)<v2) then
         sumv = sumv + (Vc(i,j)-promvc)**2
         npts = npts + 1
      endif
   end do
end do
varvc = sumv/real((npts-1))

print*,'npts =', npts, 'promvc =', promvc, 'varvc =', varvc 

print*,'paralelizacion'

np = nx2/8
!$OMP PARALLEL
!$OMP DO
do komp = 1, 8
!do l=1,nx
   l1 = komp
   l2 = komp
lloop:   do l = l1, l2
! cheat for speed?
!      if(l <=4) then
!         suma(l)=1
!         num(l)=1  
!         CYCLE lloop
!      endif
         
      lmin=real(l)-0.5
      lmax=real(l)+0.5

!print*, 'lmin', lmin, 'lmax', lmax

      do jj=ny1,ny2
         do ii=nx1, nx2

!print*, 'jj', jj, 'ii', ii

         pix=real(ii)-0.5
         piy=real(jj)-0.5
        if(Vc(ii,jj)>v1.and.Vc(ii,jj)<v2)then
!            i1 = ii
            i2=min(nx2,(ii+(int(lmax+0.5))))
!            j1=max(1,jj-(int(lmax+0.5)))
            j1 = jj
            j2=min(ny2,(jj+(int(lmax+0.5))))

            do j=j1,j2
               if(j==jj) then
                  i1 = ii
               else
                  i1=max(1,ii-(int(lmax+0.5)))
               endif
               do i=i1, i2
                  if (Vc(i,j)>v1.and.Vc(i,j)<v2)then
                     pi=real(i)-0.5
                     pj=real(j)-0.5
                     dd=(pi-pix)**2+(pj-piy)**2
                     if(sqrt(dd)>=lmin.and.sqrt(dd)<=lmax)then
                        suma(l)=suma(l)+(Vc(ii,jj) -Vc(i,j))**2
                        num(l)=num(l)+1
                     end if
                  end if
               end do
             end do
          end if
       end do
    end do
 end do lloop

print*, 'termina el loop'

   l1 = nx2 - komp*(np-1) + 1
   l2 = nx2 - komp*(np-1) + (np -1)
   do l = l1, l2
      lmin=real(l)-0.5
      lmax=real(l)+0.5

      do jj=nx1,nx2
         do ii=ny1,ny2
         
         pix=real(ii)-0.5
         piy=real(jj)-0.5
         if(Vc(ii,jj)>v1.and.Vc(ii,jj)<v2)then
!            i1=max(1,ii-(int(lmax+0.5)))
!            i1 = ii
            i2=min(nx2,(ii+(int(lmax+0.5))))
!            j1=max(1,jj-(int(lmax+0.5)))
            j1 = jj
            j2=min(ny2,(jj+(int(lmax+0.5))))

            do j=j1,j2
               if(j==jj) then
                  i1 = ii
               else
                  i1=max(1,ii-(int(lmax+0.5)))
               endif
               do i=i1, i2
                 if (Vc(i,j)>v1.and.Vc(i,j)<v2)then
                     pi=real(i)-0.5
                     pj=real(j)-0.5
                     dd=(pi-pix)**2+(pj-piy)**2
                     if(sqrt(dd)>=lmin.and.sqrt(dd)<=lmax)then
                        suma(l)=suma(l)+(Vc(ii,jj)-Vc(i,j))**2
                        num(l)=num(l)+1
                     end if
                  end if
               end do
             end do
          end if
      end do    
    end do  
 end do           
enddo
!$OMP END DO
!$OMP END PARALLEL
print*, 'termina y guarda archivo'

archivos=trim(emtype)//'-sf2-orion'//'.dat'
open(10,file=archivos,status="unknown")
do l=1,nx2     
if(num(l)==0)then
!   WRITE(6,*) l, promvc, varvc, num(l), suma(l), -999
   WRITE(10,*) l, promvc, varvc, num(l), suma(l), -999
else 
!   WRITE(6,*) l, promvc, varvc, num(l), suma(l), suma(l)/(varvc*real(num(l)))
   WRITE(10,*) l, promvc, varvc, num(l), suma(l), suma(l)/(varvc*real(num(l)))
endif
end do
close(10)   

end program funcion_estructura_omp3_mio


